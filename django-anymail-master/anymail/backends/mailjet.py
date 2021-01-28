from email.header import Header
from urllib.parse import quote

from .base_requests import AnymailRequestsBackend, RequestsPayload
from ..exceptions import AnymailRequestsAPIError
from ..message import ANYMAIL_STATUSES, AnymailRecipientStatus
from ..utils import EmailAddress, get_anymail_setting, parse_address_list


class EmailBackend(AnymailRequestsBackend):
    """
    Mailjet API Email Backend
    """

    esp_name = "Mailjet"

    def __init__(self, **kwargs):
        """Init options from Django settings"""
        esp_name = self.esp_name
        self.api_key = get_anymail_setting('api_key', esp_name=esp_name, kwargs=kwargs, allow_bare=True)
        self.secret_key = get_anymail_setting('secret_key', esp_name=esp_name, kwargs=kwargs, allow_bare=True)
        api_url = get_anymail_setting('api_url', esp_name=esp_name, kwargs=kwargs,
                                      default="https://api.mailjet.com/v3")
        if not api_url.endswith("/"):
            api_url += "/"
        super().__init__(api_url, **kwargs)

    def build_message_payload(self, message, defaults):
        return MailjetPayload(message, defaults, self)

    def raise_for_status(self, response, payload, message):
        # Improve Mailjet's (lack of) error message for bad API key
        if response.status_code == 401 and not response.content:
            raise AnymailRequestsAPIError(
                "Invalid Mailjet API key or secret",
                email_message=message, payload=payload, response=response, backend=self)
        super().raise_for_status(response, payload, message)

    def parse_recipient_status(self, response, payload, message):
        # Mailjet's (v3.0) transactional send API is not covered in their reference docs.
        # The response appears to be either:
        #   {"Sent": [{"Email": ..., "MessageID": ...}, ...]}
        #   where only successful recipients are included
        # or if the entire call has failed:
        #   {"ErrorCode": nnn, "Message": ...}
        parsed_response = self.deserialize_json_response(response, payload, message)
        if "ErrorCode" in parsed_response:
            raise AnymailRequestsAPIError(email_message=message, payload=payload, response=response,
                                          backend=self)

        recipient_status = {}
        try:
            for key in parsed_response:
                status = key.lower()
                if status not in ANYMAIL_STATUSES:
                    status = 'unknown'

                for item in parsed_response[key]:
                    message_id = str(item['MessageID'])
                    email = item['Email']
                    recipient_status[email] = AnymailRecipientStatus(message_id=message_id, status=status)
        except (KeyError, TypeError) as err:
            raise AnymailRequestsAPIError("Invalid Mailjet API response format",
                                          email_message=message, payload=payload, response=response,
                                          backend=self) from err
        # Make sure we ended up with a status for every original recipient
        # (Mailjet only communicates "Sent")
        for recipients in payload.recipients.values():
            for email in recipients:
                if email.addr_spec not in recipient_status:
                    recipient_status[email.addr_spec] = AnymailRecipientStatus(message_id=None, status='unknown')

        return recipient_status


class MailjetPayload(RequestsPayload):

    def __init__(self, message, defaults, backend, *args, **kwargs):
        self.esp_extra = {}  # late-bound in serialize_data
        auth = (backend.api_key, backend.secret_key)
        http_headers = {
            'Content-Type': 'application/json',
        }
        # Late binding of recipients and their variables
        self.recipients = {'to': []}
        self.metadata = None
        self.merge_data = {}
        self.merge_metadata = {}
        super().__init__(message, defaults, backend, auth=auth, headers=http_headers, *args, **kwargs)

    def get_api_endpoint(self):
        return "send"

    def serialize_data(self):
        self._populate_sender_from_template()
        if self.is_batch():
            self.data = {'Messages': [
                self._data_for_recipient(to_addr)
                for to_addr in self.recipients['to']
            ]}
        return self.serialize_json(self.data)

    def _data_for_recipient(self, email):
        # Return send data for single recipient, without modifying self.data
        data = self.data.copy()
        data['To'] = self._format_email_for_mailjet(email)

        if email.addr_spec in self.merge_data:
            recipient_merge_data = self.merge_data[email.addr_spec]
            if 'Vars' in data:
                data['Vars'] = data['Vars'].copy()  # clone merge_global_data
                data['Vars'].update(recipient_merge_data)
            else:
                data['Vars'] = recipient_merge_data

        if email.addr_spec in self.merge_metadata:
            recipient_metadata = self.merge_metadata[email.addr_spec]
            if self.metadata:
                metadata = self.metadata.copy()  # clone toplevel metadata
                metadata.update(recipient_metadata)
            else:
                metadata = recipient_metadata
            data["Mj-EventPayLoad"] = self.serialize_json(metadata)

        return data

    def _populate_sender_from_template(self):
        # If no From address was given, use the address from the template.
        # Unfortunately, API 3.0 requires the From address to be given, so let's
        # query it when needed. This will supposedly be fixed in 3.1 with a
        # public beta in May 2017.
        template_id = self.data.get("Mj-TemplateID")
        if template_id and not self.data.get("FromEmail"):
            response = self.backend.session.get(
                "%sREST/template/%s/detailcontent" % (self.backend.api_url, quote(str(template_id), safe='')),
                auth=self.auth, timeout=self.backend.timeout
            )
            self.backend.raise_for_status(response, None, self.message)
            json_response = self.backend.deserialize_json_response(response, None, self.message)
            # Populate email address header from template.
            try:
                headers = json_response["Data"][0]["Headers"]
                if "From" in headers:
                    # Workaround Mailjet returning malformed From header
                    # if there's a comma in the template's From display-name:
                    from_email = headers["From"].replace(",", "||COMMA||")
                    parsed = parse_address_list([from_email])[0]
                    if parsed.display_name:
                        parsed = EmailAddress(parsed.display_name.replace("||COMMA||", ","),
                                              parsed.addr_spec)
                else:
                    parsed = EmailAddress(headers["SenderName"], headers["SenderEmail"])
            except KeyError as err:
                raise AnymailRequestsAPIError("Invalid Mailjet template API response",
                                              email_message=self.message, response=response,
                                              backend=self.backend) from err
            self.set_from_email(parsed)

    def _format_email_for_mailjet(self, email):
        """Return EmailAddress email converted to a string that Mailjet can parse properly"""
        # Workaround Mailjet 3.0 bug parsing RFC-2822 quoted display-name with commas
        # (see test_comma_in_display_name in test_mailjet_backend for details)
        if "," in email.display_name:
            # Force MIME "encoded-word" encoding on name, to hide comma from Mailjet.
            # We just want the RFC-2047 quoting, not the header wrapping (which will
            # be Mailjet's responsibility), so set a huge maxlinelen.
            encoded_name = Header(email.display_name.encode('utf-8'),
                                  charset='utf-8', maxlinelen=1000000).encode()
            email = EmailAddress(encoded_name, email.addr_spec)
        return email.address

    #
    # Payload construction
    #

    def init_payload(self):
        self.data = {}

    def set_from_email(self, email):
        self.data["FromEmail"] = email.addr_spec
        if email.display_name:
            self.data["FromName"] = email.display_name

    def set_recipients(self, recipient_type, emails):
        assert recipient_type in ["to", "cc", "bcc"]
        if emails:
            self.recipients[recipient_type] = emails  # save for recipient_status processing
            self.data[recipient_type.capitalize()] = ", ".join(
                [self._format_email_for_mailjet(email) for email in emails])

    def set_subject(self, subject):
        self.data["Subject"] = subject

    def set_reply_to(self, emails):
        headers = self.data.setdefault("Headers", {})
        if emails:
            headers["Reply-To"] = ", ".join([str(email) for email in emails])
        elif "Reply-To" in headers:
            del headers["Reply-To"]

    def set_extra_headers(self, headers):
        self.data.setdefault("Headers", {}).update(headers)

    def set_text_body(self, body):
        self.data["Text-part"] = body

    def set_html_body(self, body):
        if "Html-part" in self.data:
            # second html body could show up through multiple alternatives, or html body + alternative
            self.unsupported_feature("multiple html parts")

        self.data["Html-part"] = body

    def add_attachment(self, attachment):
        if attachment.inline:
            field = "Inline_attachments"
            name = attachment.cid
        else:
            field = "Attachments"
            name = attachment.name or ""
        self.data.setdefault(field, []).append({
            "Content-type": attachment.mimetype,
            "Filename": name,
            "content": attachment.b64content
        })

    def set_envelope_sender(self, email):
        self.data["Sender"] = email.addr_spec  # ??? v3 docs unclear

    def set_metadata(self, metadata):
        self.data["Mj-EventPayLoad"] = self.serialize_json(metadata)
        self.metadata = metadata  # keep original in case we need to merge with merge_metadata

    def set_tags(self, tags):
        # The choices here are CustomID or Campaign, and Campaign seems closer
        # to how "tags" are handled by other ESPs -- e.g., you can view dashboard
        # statistics across all messages with the same Campaign.
        if len(tags) > 0:
            self.data["Tag"] = tags[0]
            self.data["Mj-campaign"] = tags[0]
            if len(tags) > 1:
                self.unsupported_feature('multiple tags (%r)' % tags)

    def set_track_clicks(self, track_clicks):
        # 1 disables tracking, 2 enables tracking
        self.data["Mj-trackclick"] = 2 if track_clicks else 1

    def set_track_opens(self, track_opens):
        # 1 disables tracking, 2 enables tracking
        self.data["Mj-trackopen"] = 2 if track_opens else 1

    def set_template_id(self, template_id):
        self.data["Mj-TemplateID"] = template_id
        self.data["Mj-TemplateLanguage"] = True

    def set_merge_data(self, merge_data):
        # Will be handled later in serialize_data
        self.merge_data = merge_data

    def set_merge_global_data(self, merge_global_data):
        self.data["Vars"] = merge_global_data

    def set_merge_metadata(self, merge_metadata):
        # Will be handled later in serialize_data
        self.merge_metadata = merge_metadata

    def set_esp_extra(self, extra):
        self.data.update(extra)
