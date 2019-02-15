import axios from 'axios'

export function fetch(method, url, params) {
  if (method === 'get' || method === 'GET') {
    return new Promise((resolve, reject) => {
      axios.get(url, {
        params: params
      }).then(res => {
        resolve(res)
      }).catch(err => {
        reject(err)
      })
    })
  } else {
    return new Promise((resolve, reject) => {
      axios.post(url, params)
        .then(res => {
          resolve(res)
        }, err => {
          reject(err)
        })
    })
  }
}

// export function fetch_post(url, params) {
//   return new Promise((resolve, reject) => {
//     axios.post(url, params)
//       .then(res => {
//         resolve(res)
//       }, err => {
//         reject(err)
//       })
//   })
// }
