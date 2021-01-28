from unittest import skip

from djangae.contrib.search import fields, IntegrityError
from djangae.contrib.search.document import Document
from djangae.contrib.search.index import Index
from djangae.contrib.search.models import TokenFieldIndex
from djangae.contrib.search.tokens import tokenize_content
from djangae.test import TestCase


class QueryStringParseTests(TestCase):
    pass


class DocumentTests(TestCase):
    def test_get_fields(self):

        class DocOne(Document):
            pass

        class DocTwo(Document):
            text = fields.TextField()
            atom = fields.AtomField()

        doc = DocOne()
        self.assertEqual(list(doc.get_fields().keys()), ['id'])

        doc2 = DocTwo()
        self.assertEqual(3, len(doc2.get_fields()))


class IndexingTests(TestCase):
    @skip("Atom fields not implemented")
    def test_indexing_atom_fields(self):
        class Doc(Document):
            atom = fields.AtomField()

        doc1 = Doc(atom="This is a test")
        doc2 = Doc(atom="This is also a test")
        doc3 = Doc(atom="This")

        index = Index(name="MyIndex")
        index.add(doc1)
        index.add(doc2)

        # Exact match, or exact field match should return doc1
        self.assertTrue(doc1 in index.search('atom:"This is a test"'))
        self.assertFalse(doc2 in index.search('atom:"This is a test"'))
        self.assertTrue(doc1 in index.search('"This is a test"'))

        # Partial match should only return exact atom matches
        self.assertTrue(doc3 in index.search('This'))
        self.assertFalse(doc1 in index.search('This'))
        self.assertFalse(doc2 in index.search('This'))

    def test_indexing_text_fields(self):
        class Doc(Document):
            text = fields.TextField()

        doc = Doc(text="This is a test. Cheese.")
        doc2 = Doc(text="This is also a test. Pickle.")

        index = Index(name="My Index")
        index.add(doc)
        index.add(doc2)

        # We should have some generated IDs now
        self.assertTrue(doc.id)
        self.assertTrue(doc2.id)

        results = [x for x in index.search("test", document_class=Doc)]

        # Both documents should have come back
        self.assertCountEqual(
            [doc.id, doc2.id],
            [x.id for x in results]
        )

        results = [x for x in index.search("TEST", document_class=Doc)]

        # Both documents should have come back
        self.assertCountEqual(
            [doc.id, doc2.id],
            [x.id for x in results]
        )

        results = [x for x in index.search("cheese OR pickle", document_class=Doc)]

        # Both documents should have come back
        self.assertCountEqual(
            [doc.id, doc2.id],
            [x.id for x in results]
        )

        results = [x for x in index.search('cheese OR text:pickle', document_class=Doc)]

        # Both documents should have come back
        self.assertCountEqual(
            [doc.id, doc2.id],
            [x.id for x in results]
        )

        # FIXME: Uncomment when exact matching is implemented
        # results = [x for x in index.search('"cheese" OR pickle', document_class=Doc)]

        # # Both documents should have come back
        # self.assertCountEqual(
        #   [doc.id, doc2.id],
        #   [x.id for x in results]
        # )

    def test_removing_document(self):

        class Doc(Document):
            text = fields.TextField()

        i0 = Index(name="index1")
        i1 = Index(name="index2")

        d0 = i0.add(Doc(text="One"))

        # One field, one token
        self.assertEqual(
            TokenFieldIndex.objects.count(),
            1
        )

        self.assertEqual(i0.document_count(), 1)
        self.assertEqual(i1.document_count(), 0)

        d1 = i0.add(Doc(text="Two"))

        # Two fields, one token each
        self.assertEqual(
            TokenFieldIndex.objects.count(),
            2
        )

        self.assertEqual(i0.document_count(), 2)
        self.assertEqual(i1.document_count(), 0)

        d2 = i1.add(Doc(text="Three 3"))

        # Three fields, one token each except last which has 2
        self.assertEqual(
            TokenFieldIndex.objects.count(),
            4
        )

        self.assertEqual(i0.document_count(), 2)
        self.assertEqual(i1.document_count(), 1)

        self.assertTrue(i0.remove(d0))
        self.assertFalse(i0.remove(d0))

        self.assertEqual(i0.document_count(), 1)
        self.assertEqual(i1.document_count(), 1)

        self.assertEqual(
            TokenFieldIndex.objects.count(),
            3
        )

        self.assertFalse([x for x in i0.search("text:One", Doc)])

        self.assertTrue(i0.remove(d1))

        self.assertEqual(i0.document_count(), 0)
        self.assertEqual(i1.document_count(), 1)

        self.assertEqual(
            TokenFieldIndex.objects.count(),
            2
        )

        self.assertFalse([x for x in i0.search("text:Two", Doc)])

        self.assertTrue(i1.remove(d2))

        self.assertEqual(i0.document_count(), 0)
        self.assertEqual(i1.document_count(), 0)

        self.assertEqual(
            TokenFieldIndex.objects.count(),
            0
        )

        self.assertFalse([x for x in i1.search("text:Three", Doc)])
        self.assertFalse([x for x in i1.search("text:3", Doc)])

    def test_pipe_not_indexed(self):
        """
            The | symbols is used for TokenFieldIndex key generation
            so shouldn't be indexed... ever!
        """

        class Doc(Document):
            name = fields.TextField()

        index = Index(name="test")
        index.add(Doc(name="|| Pipes"))

        self.assertEqual(index.document_count(), 1)
        self.assertEqual(TokenFieldIndex.objects.count(), 1)  # Just "pipes"

    def test_tokenization_of_acronyms(self):
        """
            Hyphens are stop characters except when they are part
            of an ancronym (e.g I-B-M), this handling also covers dates
            (e.g. 2020-01-01)
        """
        text = "This-is some text with - hyphens. I-B-M"
        tokens, new_tokens = tokenize_content(text)
        self.assertCountEqual(
            tokens + new_tokens,
            ["This", "-", "is", "some", "text", "with", "-", "hyphens", ".", "I-B-M", "IBM", "I.B.M"]
        )

    def test_null_validation(self):
        """
            If a field is marked as null=False, and someone tries to index
            None, then an IntegrityError should throw. None of the documents
            should be indexed if one of them is invalid.
        """

        class Doc(Document):
            text = fields.TextField(null=False)

        index = Index("test")
        doc1 = Doc(text="test")
        doc2 = Doc(text=None)

        self.assertRaises(IntegrityError, index.add, [doc1, doc2])
        self.assertEqual(index.document_count(), 0)  # Nothing should've been indexed

    def test_field_index_flag_respected(self):
        class Doc(Document):
            text = fields.TextField()
            other_text = fields.TextField(index=False)

        index = Index("test")
        doc1 = Doc(text="foo", other_text="bar")
        doc2 = Doc(text="bar", other_text="foo")

        index.add([doc1, doc2])

        results = list(index.search("foo", Doc))
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].text, "foo")
        self.assertEqual(results[0].other_text, "bar")

        results = list(index.search("bar", Doc))
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].text, "bar")
        self.assertEqual(results[0].other_text, "foo")

    def test_stopwords_indexed(self):
        """
            Stop words should be indexed. They should be ranked lower
            and not included in searches if match_stopwords is False
        """

        class Doc(Document):
            text = fields.TextField()

        index = Index("test")
        doc1 = Doc(text="about")
        index.add(doc1)

        self.assertTrue(list(index.search("about", Doc)))
        self.assertTrue(list(index.search("abo", Doc, use_startswith=True)))
        self.assertFalse(list(index.search("about", Doc, match_stopwords=False)))

        # Startswith matching overrides matching of stopwords (as other tokens may start with the stop word)
        self.assertTrue(list(index.search("about", Doc, use_startswith=True, match_stopwords=False)))
