import request from '@/utils/request'

export function login(data) {
  return request({
    url: '/user/login',
    method: 'post',
    data
  })
}

export function getInfo() {
  return request({
    url: '/user/userinfo',
    method: 'get'

  })
}
export function putUserInfo(data) {
  return request({
    url: '/user/userinfo',
    method: 'put',
    data
  })
}

export function logout() {
  return request({
    url: '/user/logout',
    method: 'post'
  })
}


export function getDepartment(params) {
  return request({
    url: '/user/department',
    method: 'get',
    params
  })
}

export function postDepartment(data) {
  return request({
    url: '/user/department',
    method: 'post',
    data
  })
}
//params
export function putDepartment(data, pk) {
  return request({
    url: '/user/department/' + pk,
    method: 'put',
    data

  })
}
export function deleteDepartment(pk) {
  return request({
    url: '/user/department/' + pk,
    method: 'delete'
  })
}


export function getUserManagement(params) {
  return request({
    url: '/user/management',
    method: 'get',
    params
  })
}

export function postUserManagement(data) {
  return request({
    url: '/user/management',
    method: 'post',
    data
  })
}
//params
export function putUserManagement(data, pk) {
  return request({
    url: '/user/management/' + pk,
    method: 'put',
    data

  })
}
export function deleteUserManagement(pk) {
  return request({
    url: '/user/management/' + pk,
    method: 'delete'
  })
}

export function detailsUserManagement(pk) {
  return request({
    url: '/user/management/' + pk,
    method: 'get'
  })
}

// export function logout() {
//   return request({
//     url: '/user/logout',
//     method: 'post'
//   })
// }
//
// export function logout() {
//   return request({
//     url: '/user/logout',
//     method: 'post'
//   })
// }
