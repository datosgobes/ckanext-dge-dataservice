# Copyright (C) 2025 Entidad Pública Empresarial Red.es
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

import ckan.plugins.toolkit as toolkit




def create(context, data_dict):
    '''Create a Dataservice.
    
    '''
    return toolkit.check_access('package_create')(context, data_dict)


def delete(context, data_dict):
    '''Delete a Dataservice.
    
    '''
    return toolkit.check_access('package_delete')(context, data_dict)


def update(context, data_dict):
    '''Update a Dataservice.
    
    '''
    return toolkit.check_access('package_update')(context, data_dict)


@toolkit.auth_allow_anonymous_access
def show(context, data_dict):
    '''All users can access a dataservice show'''
    return {'success': True}


@toolkit.auth_allow_anonymous_access
def dataservice_list(context, data_dict):
    '''All users can access a dataservice list'''
    return {'success': True}

@toolkit.auth_allow_anonymous_access
def organization_dataservice_list(context, data_dict):
    '''All users can access a organization dataservice list'''
    return {'success': True}

def package_association_create(context, data_dict):
    '''Create a package dataservice association.
    
    '''
    return toolkit.check_access('package_create')(context, data_dict)


def package_association_delete(context, data_dict):
    '''Delete a package dataservice association.
    
    '''
    return toolkit.check_access('package_create')(context, data_dict)


@toolkit.auth_allow_anonymous_access
def dataservice_package_list(context, data_dict):
    '''All users can access a dataservice's package list'''
    return {'success': True}



@toolkit.auth_allow_anonymous_access
def dataservice_package_list(context, data_dict):
    '''All users can access a dataservice's package list'''
    return {'success': True}

@toolkit.auth_allow_anonymous_access
def package_dataservice_list(context, data_dict):
    '''All users can access a packages's dataservice list'''
    return {'success': True}


def dataservice_package_association_create(context, data_dict):
    '''Create a package dataservice association.

       Only sysadmins or user listed as Dataservice Admins can create a
       package/dataservice association.
    '''
    return toolkit.check_access('package_update')(context, data_dict)


def dataservice_package_association_delete(context, data_dict):
    '''Delete a package dataservice association.

       Only user listed as Organization editors can delete a
       package/dataservice association.
    '''
    return toolkit.check_access('package_update')(context, data_dict)