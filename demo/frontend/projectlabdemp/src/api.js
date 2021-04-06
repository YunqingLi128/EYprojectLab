import axios from 'axios'

const baseUrl = 'http://127.0.0.1:5000/'
const corsHeaders = {
  'secret-key': 'super secret key',
  'Access-Control-Allow-Origin': '*'
}
let reqConfig = {
  params: {},
  withCredentials: true,
  headers: corsHeaders
}

export default {
  initData (endpoint) {
    let reqUrl = baseUrl + endpoint
    return axios.get(reqUrl, {
      withCredentials: true,
      headers: corsHeaders
    })
  },
  addData (endpoint, id, name, nickName) {
    let reqUrl = baseUrl + endpoint
    reqConfig.params = {
      'rssd_id': id,
      'name': name,
      'nickName': nickName
    }
    // TODO: post method will encounter CORS problem
    return axios.get(reqUrl, reqConfig)
  },
  getDataByQuarter (endpoint, quarter) {
    let reqUrl = baseUrl + endpoint
    reqConfig.params = {
      'quarter': quarter
    }
    return axios.get(reqUrl, reqConfig)
  },
  getDataOvertime (endpoint, start, end) {
    let reqUrl = baseUrl + endpoint
    reqConfig.params = {
      'start': start,
      'end': end
    }
    return axios.get(reqUrl, reqConfig)
  }
}
