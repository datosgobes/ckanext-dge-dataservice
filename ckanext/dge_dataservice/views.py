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
import ckan.lib.helpers as h
import ckan.plugins.toolkit as tk
import ckan.views.dataset as dataset
import ckanext.dge_dataservice.utils as utils

from flask import Blueprint
from ckan.plugins.toolkit import _, request
from ckan.lib.search import SearchIndexError

log = logging.getLogger(__name__)


bp_dataservice = Blueprint(utils.DATASERVICE_BLUEPRINT_NAME, __name__, 
    url_defaults={u'package_type': u'dataservice'})

def index():
    return dataset.search(utils.DATASERVICE_TYPE_NAME)

def search():
    return dataset.search(utils.DATASERVICE_TYPE_NAME)


class CreateView(dataset.CreateView):
    def post(self):
    
        # The staged add dataset used the new functionality when the dataset is
        # partially created so we need to know if we actually are updating or
        # this is a real new.
        context = self._prepare()
        try:
            data_dict = dataset.clean_dict(
                dataset.dict_fns.unflatten(dataset.tuplize_dict(dataset.parse_params(request.form)))
            )
        except dataset.dict_fns.DataError:
            return tk.base.abort(400, _(u'Integrity Error'))
        try:
            pkg_dict = tk.get_action(u'dge_dataservice_dataservice_create')(context, data_dict)
            url = h.url_for(u'{0}.read'.format(utils.DATASERVICE_TYPE_NAME), id=pkg_dict['name'])
            return h.redirect_to(url)
        except tk.NotAuthorized:
            return tk.base.abort(403, _(u'Unauthorized to read dataservice'))
        except tk.ObjectNotFound as e:
            return tk.base.abort(404, _(u'Dataservice not found'))
        except SearchIndexError as e:
            try:
                exc_str = tk.text_type(repr(e.args))
            except Exception: 
                exc_str = tk.text_type(str(e))
            return tk.base.abort(
                500,
                _(u'Unable to add dataservice to search index.') + exc_str
            )
        except tk.ValidationError as e:
            errors = e.error_dict
            error_summary = e.error_summary
            data_dict[u'state'] = u'none'
            return self.get(data_dict, errors, error_summary)
    
    def get(self, data=None, errors=None, error_summary=None):
        utils.check_new_view_auth()
        return super(CreateView, self).get(utils.DATASERVICE_TYPE_NAME, data, errors, error_summary)


class EditView(dataset.EditView):
    def get(self, id, data=None, errors=None, error_summary=None):
        utils.check_new_view_auth()
        return super(EditView, self).get(utils.DATASERVICE_TYPE_NAME, id, data,
                                         errors, error_summary)

    def post(self, id):
        context = self._prepare(id)

        utils.check_edit_view_auth(id)

        data_dict = dataset.clean_dict(
            dataset.dict_fns.unflatten(
                dataset.tuplize_dict(dataset.parse_params(tk.request.form))))
        data_dict.update(
            dataset.clean_dict(
                dataset.dict_fns.unflatten(
                    dataset.tuplize_dict(dataset.parse_params(
                        tk.request.files)))))

        data_dict['id'] = id
        try:
            pkg = tk.get_action('dge_dataservice_dataservice_update')(context, data_dict)
        except tk.ValidationError as e:
            errors = e.error_dict
            error_summary = e.error_summary
            return self.get(id, data_dict, errors, error_summary)

        tk.c.pkg_dict = pkg

        url = h.url_for(f'{utils.DATASERVICE_BLUEPRINT_NAME}.read', id=pkg['name'])
        return h.redirect_to(url)
        
def read(id):
    return utils.read_view(id)

def dataset_dataservices_list(id):
    return utils.dataset_dataservice_list(id)


def delete_dataservice(id, package_type):
    return utils.delete_view(id)

bp_dataservice.add_url_rule(f'/{utils.DATASERVICE_TYPE_NAME}/', 
                            view_func = index,
                            endpoint = 'index')

bp_dataservice.add_url_rule(f'/{utils.DATASERVICE_TYPE_NAME}', 
                            view_func = search,
                            endpoint = 'search')

bp_dataservice.add_url_rule(f'/{utils.DATASERVICE_TYPE_NAME}/new', 
                            view_func = CreateView.as_view(str(u'new')),
                            endpoint = 'new')

bp_dataservice.add_url_rule(f'/{utils.DATASERVICE_TYPE_NAME}/<id>', 
                            view_func=read, 
                            endpoint="read")

bp_dataservice.add_url_rule(f'/{utils.DATASERVICE_TYPE_NAME}/edit/<id>',
                      view_func=EditView.as_view('edit'),
                      methods=['GET', 'POST'],
                      endpoint="edit")

bp_dataservice.add_url_rule(f'/{utils.DATASET_TYPE_NAME}/{utils.DATASERVICE_TYPE_NAME}s/<id>',
                      view_func=dataset_dataservices_list,
                      methods=['GET', 'POST'],
                      endpoint="dataset_dataservice_list")

bp_dataservice.add_url_rule(f'/{utils.DATASERVICE_TYPE_NAME}/delete/<id>',
                      defaults={u'package_type': u'dataservice'},
                      view_func=delete_dataservice,
                      methods=['GET', 'POST'],
                      endpoint="delete")

def get_blueprints():
    return [bp_dataservice]