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

import ckanext.dge_dataservice.logic.action.create
import ckanext.dge_dataservice.logic.action.get
import ckanext.dge_dataservice.logic.action.delete
import ckanext.dge_dataservice.logic.action.update

def get_actions():
    action_functions = {
        'dge_dataservice_dataservice_show': ckanext.dge_dataservice.logic.action.get.dataservice_show,
        'dge_dataservice_dataservice_create': ckanext.dge_dataservice.logic.action.create.dataservice_create,
        'dge_dataservice_dataservice_update': ckanext.dge_dataservice.logic.action.update.dataservice_update,
        'dge_dataservice_dataservice_delete': ckanext.dge_dataservice.logic.action.delete.dataservice_delete,
        'dge_dataservice_dataservice_list': ckanext.dge_dataservice.logic.action.get.dataservice_list,
        'dge_dataservice_organization_dataservice_list': ckanext.dge_dataservice.logic.action.get.organization_dataservice_list,
        }
    return action_functions