import axios from 'axios'
axios.defaults.withCredentials = true
export function fetch(method, url, params) {
  let realUrl = 'http://localhost:5000/' + url
  if (method === 'get' || method === 'GET') {
    return new Promise((resolve, reject) => {
      axios.get(realUrl, {
        params: params
      }).then(res => {
        resolve(res)
      }).catch(err => {
        reject(err)
      })
    })
  } else {
    return new Promise((resolve, reject) => {
      axios.post(realUrl, params)
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
