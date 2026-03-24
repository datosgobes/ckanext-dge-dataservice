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

from urllib.parse import urlencode

import ckan.model as model
import ckan.lib.helpers as h
import ckan.plugins.toolkit as tk


_ = tk._
abort = tk.abort

log = logging.getLogger(__name__)

DATASET_TYPE_NAME = 'dataset'
DATASERVICE_TYPE_NAME = 'dataservice'
DATASERVICE_BLUEPRINT_NAME = 'dgeDataserviceBlueprint'

def check_edit_view_auth(id):
    context = {
        'model': model,
        'session': model.Session,
        'user': tk.g.user or tk.g.author,
        'auth_user_obj': tk.g.userobj,
        'save': 'save' in tk.request.args,
        'pending': True
    }

    try:
        tk.check_access('dge_dataservice_dataservice_update', context)
    except tk.NotAuthorized:
        return tk.abort(
            401,
            _('User not authorized to edit {dataservice_id}').format(
                dataservice_id=id))


def check_new_view_auth():
    context = {
        'model': model,
        'session': model.Session,
        'user': tk.g.user or tk.g.author,
        'auth_user_obj': tk.g.userobj,
        'save': 'save' in tk.request.args
    }

    # Check access here, then continue with PackageController.new()
    # PackageController.new will also check access for package_create.
    try:
        tk.check_access('dge_dataservice_dataservice_create', context)
    except tk.NotAuthorized:
        return tk.abort(401, _('Unauthorized to create a dataservice'))


def _encode_params(params):
    return [(k, str(v)) for k, v in params]


def url_with_params(url, params):
    params = _encode_params(params)
    return url + '?' + urlencode(params)


def convert_package_name_or_id_to_title_or_name(package_name_or_id, context):
    '''
    Return the package title, or name if no title, for the given package name
    or id.

    :returns: the name of the package with the given name or id
    :rtype: string
    :raises: ckan.lib.navl.dictization_functions.Invalid if there is no
        package with the given name or id

    '''
    session = context['session']
    result = session.query(model.Package).filter_by(
            id=package_name_or_id).first()
    if not result:
        result = session.query(model.Package).filter_by(
                name=package_name_or_id).first()
    if not result:
        raise tk.Invalid('%s: %s' % (_('Not found'), _('Dataset')))
    return result.title or result.name


def read_view(id):
    context = {
        'model': model,
        'session': model.Session,
        'user': tk.g.user or tk.g.author,
        'for_view': True,
        'auth_user_obj': tk.g.userobj
    }
    data_dict = {'id': id}

    try:
        tk.g.pkg_dict = tk.get_action('package_show')(context, data_dict)
    except tk.ObjectNotFound:
        return tk.abort(404, _('Dataservice not found'))
    except tk.NotAuthorized:
        return tk.abort(401, _('Unauthorized to read dataservice'))


    return tk.render('dataservice/read.html',
                     extra_vars={'dataset_type': DATASERVICE_TYPE_NAME})

def dataset_dataservice_list(id):
    context = {
        'model': model,
        'session': model.Session,
        'user': tk.g.user or tk.g.author,
        'for_view': True,
        'auth_user_obj': tk.g.userobj
    }
    data_dict = {'id': id}

    try:
        tk.check_access('package_show', context, data_dict)
    except tk.ObjectNotFound:
        return tk.abort(404, _('Dataset not found'))
    except tk.NotAuthorized:
        return tk.abort(401, _('Not authorized to see this page'))

    try:
        tk.g.pkg_dict = tk.get_action('package_show')(context, data_dict)
        tk.g.dataservice_list = tk.get_action('dge_dataservice_package_dataservice_list')(
            context, {
                'package_id': tk.g.pkg_dict['id']
            })
        log.debug(f'[dataset_dataservice_list] package_id={tk.g.pkg_dict["id"]} dataservice_list={tk.g.dataservice_list}')
    except tk.ObjectNotFound:
        return tk.abort(404, _('Dataset not found'))
    except tk.NotAuthorized:
        return tk.abort(401, _('Unauthorized to read package'))

    list_route = f'{DATASERVICE_BLUEPRINT_NAME}.dataset_dataservice_list'

    if tk.request.method == 'POST':
        form_data = tk.request.form
        new_dataservice = form_data.get('dataservice_added')
        log.debug(f'[dataset_dataservice_list] new_dataservice = {new_dataservice}')
        if new_dataservice:
            data_dict = {
                "dataservice_id": new_dataservice,
                "package_id": tk.g.pkg_dict['id']
            }
            try:
                tk.get_action('dge_dataservice_dataservice_package_association_create')(
                    context, data_dict)
            except tk.ObjectNotFound:
                return tk.abort(404, _('Dataservice not found'))
            else:
                h.flash_success(
                    _("The dataset has been added to the dataservice."))

        dataservice_to_remove = form_data.get('remove_dataservice_id')
        if dataservice_to_remove:
            data_dict = {
                "dataservice_id": dataservice_to_remove,
                "package_id": tk.g.pkg_dict['id']
            }
            try:
                tk.get_action('dge_dataservice_dataservice_package_association_delete')(
                    context, data_dict)
            except tk.ObjectNotFound:
                return tk.abort(404, _('Dataservice not found'))
            else:
                h.flash_success(
                    _("The dataset has been removed from the dataservice."))
        return h.redirect_to(
            h.url_for(list_route, id=tk.g.pkg_dict['name']))

    pkg_dataservice_ids = [dataservice['id'] for dataservice in tk.g.dataservice_list]
    site_dataservices = tk.get_action('dge_dataservice_dataservice_list')(context, {})

    tk.g.dataservice_dropdown = [[dataservice['id'], dataservice['title']]
                           for dataservice in site_dataservices
                           if dataservice['id'] not in pkg_dataservice_ids]

    return tk.render("package/dataset_dataservice_list.html",
                     extra_vars={'pkg_dict': tk.g.pkg_dict})


def delete_view(id):
    if 'cancel' in tk.request.args:
        tk.redirect_to(f'{DATASERVICE_BLUEPRINT_NAME}.edit', id=id)

    context = {
        'model': model,
        'session': model.Session,
        'user': tk.g.user or tk.g.author,
        'auth_user_obj': tk.g.userobj
    }

    try:
        tk.check_access('dge_dataservice_dataservice_delete', context, {'id': id})
    except tk.NotAuthorized:
        return tk.abort(401, _('Unauthorized to delete dataservice'))

    index_route = f'{DATASERVICE_BLUEPRINT_NAME}.index'

    context = {'user': tk.g.user}
    try:
        if tk.request.method == 'POST':
            tk.get_action('dge_dataservice_dataservice_delete')(context, {'id': id})
            h.flash_notice(_('Dataservice has been deleted.'))
            return tk.redirect_to(index_route)
        tk.g.pkg_dict = tk.get_action('package_show')(context, {'id': id})
    except tk.NotAuthorized:
        tk.abort(401, _('Unauthorized to delete dataservice'))
    except tk.ObjectNotFound:
        tk.abort(404, _('Dataservice not found'))

    return tk.render('dataservice/confirm_delete.html',
                     extra_vars={'dataset_type': DATASERVICE_TYPE_NAME})