# Copyright (C) 2026 Entidad Pública Empresarial Red.es
#
# This file is part of "dge-dataservice (datos.gob.es)".
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

# -*- coding: utf-8 -*-
import logging

import ckan.plugins as plugins
import ckan.plugins.toolkit as tk
import ckan.lib.plugins as lib_plugins
import ckan.lib.helpers as h

import ckanext.dge_dataservice.helpers as dge_dataservice_helpers

import ckanext.dge.helpers as dh

from ckanext.dge_dataservice import utils
from ckanext.dge_dataservice import views
from ckanext.dge_dataservice import validators
from ckanext.dge_dataservice.logic import auth, action

from collections import OrderedDict


log = logging.getLogger(__name__)

DATASERVICE_TYPE_NAME = utils.DATASERVICE_TYPE_NAME


class DgeDataservicePlugin(plugins.SingletonPlugin, lib_plugins.DefaultTranslation):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IFacets, inherit=True)
    plugins.implements(plugins.IAuthFunctions)
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.IPackageController, inherit=True)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IBlueprint)
    plugins.implements(plugins.ITranslation)

    # IBlueprint
    def get_blueprint(self):
        return [views.bp_dataservice]

    # IConfigurer
    def update_config(self, config_):
        tk.add_template_directory(config_, 'templates')
        tk.add_public_directory(config_, 'public')
        tk.add_resource('assets',
            'dge_dataservice')
    
    # ITemplateHelpers
    def get_helpers(self):
        return {
            'dge_dataservice_get_dataservice': dge_dataservice_helpers.get_dataservice,
            'dge_dataservice_dataservice_list': dge_dataservice_helpers.get_dataservice_list,
            'dge_dataservice_organization_dataservice_list': dge_dataservice_helpers.get_organization_dataservice_list
        }
    
    # IFacets
    def dataset_facets(self, facets_dict, package_type):
        '''Only show tags for Showcase search list.'''
        if package_type != DATASERVICE_TYPE_NAME or not dh.dge_is_frontend():
            return facets_dict
        
        lang_code = tk.request.environ['CKAN_LANG']
        facets_dict.clear()
        facets_dict['is_hvd'] = plugins.toolkit._('High-Value Dataservice')
        facets_dict['theme_id'] = plugins.toolkit._('Category')
        facets_dict['publisher_display_name'] = plugins.toolkit._('Publisher')
        tag_key = 'tags_' + lang_code
        facets_dict[tag_key] = plugins.toolkit._('Tag')

        return facets_dict

    # IAuthFunctions
    def get_auth_functions(self):
        return auth.get_auth_functions()

    # IActions
    def get_actions(self):
        return action.get_actions()

    # IPackageController
    # https://docs.ckan.org/en/2.9/extensions/plugin-interfaces.html#ckan.plugins.interfaces.IPackageController
    def _add_to_pkg_dict(self, context, pkg_dict):
        '''Add key/values to pkg_dict and return it.'''

        if pkg_dict['type'] != 'dataservice':
            return pkg_dict

        return pkg_dict
    
    def after_show(self, context, pkg_dict):
        '''Modify package_show pkg_dict.'''
        pkg_dict = self._add_to_pkg_dict(context, pkg_dict)

    def before_view(self, pkg_dict):
        '''Modify pkg_dict that is sent to templates.'''
        
        context = {'user': tk.g.user or tk.g.author}

        return self._add_to_pkg_dict(context, pkg_dict)

    def before_index(self, data_dict):
        '''
        When the package type is "dataservice", the dataservice_pkgs key is removed
        to prevent indexing errors, as it is created during visualization.
        '''
        if data_dict.get('type') == 'dataservice':
            data_dict.pop("dataservice_pkgs", None)
        
        return data_dict
    
    def before_search(self, search_params):
        '''
        Unless the query is already being filtered by this dataset_type
        (either positively, or negatively), exclude datasets of type
        `dataservice`.
        '''
        fq = search_params.get('fq', '')
        filter = 'dataset_type:{0}'.format(DATASERVICE_TYPE_NAME)
        if filter not in fq:
            search_params.update({'fq': fq + " -" + filter})
        return search_params



