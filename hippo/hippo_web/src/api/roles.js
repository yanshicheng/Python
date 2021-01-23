import request from "@/utils/request";

export function getRoles(params) {
  return request({
    url: '/user/roles',
    method: 'get',
    params
  })
}

export function postRoles(data) {
  return request({
    url: '/user/roles',
    method: 'post',
    data
  })
}
//params
export function putRoles(data, pk) {
  return request({
    url: '/user/roles/' + pk,
    method: 'put',
    data

  })
}
export function deleteRoles(pk) {
  return request({
    url: '/user/roles/' + pk,
    method: 'delete'
  })
}

export function detailsRoles(pk) {
  return request({
    url: '/user/roles/' + pk,
    method: 'get'
  })
}


export function getPermissions(params) {
  return request({
    url: '/user/permissions',
    method: 'get',
    params
  })
}
export function getPermissionsData() {
  return request({
    url: '/user/permissions-data',
    method: 'get',
  })
}
export function postPermissions(data) {
  return request({
    url: '/user/permissions',
    method: 'post',
    data
  })
}
//params
export function putPermissions(data, pk) {
  return request({
    url: '/user/permissions/' + pk,
    method: 'put',
    data

  })
}
export function deletePermissions(pk) {
  return request({
    url: '/user/permissions/' + pk,
    method: 'delete'
  })
}

export function detailsPermissions(pk) {
  return request({
    url: '/user/permissions/' + pk,
    method: 'get'
  })
}



export function getMenus(params) {
  return request({
    url: '/user/menus',
    method: 'get',
    params
  })
}

export function postMenus(data) {
  return request({
    url: '/user/menus',
    method: 'post',
    data
  })
}
//params
export function putMenus(data, pk) {
  return request({
    url: '/user/menus/' + pk,
    method: 'put',
    data

  })
}
export function deleteMenus(pk) {
  return request({
    url: '/user/menus/' + pk,
    method: 'delete'
  })
}

export function detailsMenus(pk) {
  return request({
    url: '/user/menus/' + pk,
    method: 'get'
  })
}
