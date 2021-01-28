import React from 'react';

import {mountWithTheme} from 'sentry-test/enzyme';
import {findOption, openMenu} from 'sentry-test/select';

import MemberListStore from 'app/stores/memberListStore';
import OwnerInput from 'app/views/settings/project/projectOwnership/ownerInput';

jest.mock('jquery');
describe('Project Ownership Input', function () {
  let org;
  let project;
  let put;

  beforeEach(function () {
    org = TestStubs.Organization();
    project = TestStubs.Project();

    MockApiClient.addMockResponse({
      url: '/organizations/org-slug/members/',
      method: 'GET',
      body: TestStubs.Members(),
    });
    put = MockApiClient.addMockResponse({
      url: `/projects/${org.slug}/${project.slug}/ownership/`,
      method: 'PUT',
      body: {raw: 'url:src @dummy@example.com'},
    });
    MemberListStore.loadInitialData([
      TestStubs.User({id: '1', email: 'bob@example.com'}),
    ]);
  });

  afterEach(function () {
    MemberListStore.init();
  });

  it('renders', function () {
    const wrapper = mountWithTheme(
      <OwnerInput
        params={{orgId: org.slug, projectId: project.slug}}
        organization={org}
        initialText="url:src @dummy@example.com"
        project={project}
      />,
      TestStubs.routerContext()
    );

    const submit = wrapper.find('SaveButton button');

    expect(put).not.toHaveBeenCalled();

    // if text is unchanged, submit button is disabled
    submit.simulate('click');
    expect(put).not.toHaveBeenCalled();

    wrapper.find('StyledTextArea').simulate('change', {target: {value: 'new'}});

    submit.simulate('click');

    expect(put).toHaveBeenCalled();

    expect(wrapper.find(OwnerInput)).toSnapshot();
  });

  it('updates on add preserving existing text', async function () {
    const wrapper = mountWithTheme(
      <OwnerInput
        params={{orgId: org.slug, projectId: project.slug}}
        organization={org}
        initialText="url:src @dummy@example.com"
        project={project}
      />,
      TestStubs.routerContext()
    );

    // Set a path, as path is selected bu default.
    const pathInput = wrapper.find('RuleBuilder BuilderInput');
    pathInput.simulate('change', {target: {value: 'file.js'}});

    // Select the user.
    let userSelect = wrapper.find('RuleBuilder SelectOwners');
    openMenu(userSelect, {control: true});
    await tick();
    await wrapper.update();

    // Because this menu is async we can't use selectByValue()
    userSelect = wrapper.find('RuleBuilder SelectOwners');
    findOption(userSelect, {value: 'user:1'}, {control: true})
      .at(0)
      .simulate('mouseDown');
    await wrapper.update();

    // Add the new rule.
    const button = wrapper.find('RuleBuilder AddButton button');
    button.simulate('click');

    expect(put).toHaveBeenCalledWith(
      '/projects/org-slug/project-slug/ownership/',
      expect.objectContaining({
        data: {
          raw: 'url:src @dummy@example.com' + '\n' + 'path:file.js bob@example.com',
        },
      })
    );
  });
});