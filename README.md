# edc-data-manager ![Build Status](https://github.com/potlako-code-space/potlako/actions/workflows/django.yml/badge.svg) [![codecov](https://codecov.io/gh/potlako-code-space/potlako/branch/develop/graph/badge.svg?token=2e5ca624-4d88-43b8-96f5-37a3e4617cc7)](https://codecov.io/gh/potlako-code-space/potlako)

This module registers data related issues and actions them to individuals tacking the issues.

The module works with edc-subject-dashboard and the project dashboard class

Data manager classes


To customise choices for assignees do the following:

### `Usage` 
	
	from edc_data_manager.apps import AppConfig as BaseEdcDataManagerAppConfig

	class EdcDataManagerAppConfig(BaseEdcDataManagerAppConfig):
    extra_assignee_choices = {
        'td_clinic': [
            ('td_clinic', 'TD Clinic'),
            ['test@gmail.com', 'test2@gmail.com']],
        'td_ras': [
            ('td_ras', 'TD RAs'),
            ['test3@gmail.com', 'test4@gmail.com']],
        'se_dmc': [
            ('data_management_team', 'Data Management team'),
            ['data_manager1@gmail.com', 'data_manager2@gmail.com']]}
	    identifier_pattern = '[0-9]{3}-[0-9]+'


Groups
----------

1. Create a group with name: `assignable users
2. Add all the users who need to be in the choices for assignees.


How it works
----------

Refer to the home page after installation for useage.

