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
import ckan.model as model

from ckan.plugins import toolkit as tk
from ckanext.dge_dataservice.utils import DATASET_TYPE_NAME, DATASERVICE_TYPE_NAME




log = logging.getLogger(__name__)

_ = tk._
Invalid = tk.Invalid


def convert_package_name_or_id_to_id_for_type(package_name_or_id,
                                              context, package_type=DATASET_TYPE_NAME):
    '''
    Return the id for the given package name or id. Only works with packages
    of type package_type.

    Also validates that a package with the given name or id exists.

    :returns: the id of the package with the given name or id
    :rtype: string
    :raises: ckan.lib.navl.dictization_functions.Invalid if there is no
        package with the given name or id

    '''
    session = context['session']
    model = context['model']
    result = session.query(model.Package) \
        .filter_by(id=package_name_or_id, type=package_type).first()
    if not result:
        result = session.query(model.Package) \
            .filter_by(name=package_name_or_id, type=package_type).first()
    if not result:
        raise Invalid('%s: %s' % (_('Not found'), _('Dataset')))
    return result.id


def convert_package_name_or_id_to_id_for_type_dataset(package_name_or_id,
                                                      context):
    return convert_package_name_or_id_to_id_for_type(package_name_or_id,
                                                     context,
                                                     package_type=DATASET_TYPE_NAME)


def convert_package_name_or_id_to_id_for_type_dataservice(package_name_or_id,
                                                       context):
    return convert_package_name_or_id_to_id_for_type(package_name_or_id,
                                                     context,
                                                     package_type=DATASERVICE_TYPE_NAME)
