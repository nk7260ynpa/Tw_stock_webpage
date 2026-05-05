import axios from 'axios'

// 支援 Dashboard 反向代理：BASE_URL 由 Vite build 時注入
// - 本地獨立存取：BASE_URL='/'（直接打到後端根路徑）
// - Dashboard 代理：BASE_URL='/app/webpage/'（帶前綴存取）
// 確保 baseURL 不以斜線結尾，避免雙斜線
const BASE = import.meta.env.BASE_URL.replace(/\/$/, '')

const api = axios.create({
  baseURL: `${BASE}/api`,
  timeout: 30000,
})

/** 取得所有股票清單 */
export const fetchStocks = async () => {
  const { data } = await api.get('/stocks')
  return data.stocks
}

/** 取得股價歷史與技術指標 */
export const fetchPriceHistory = async (code, start, end) => {
  const params = {}
  if (start) params.start = start
  if (end) params.end = end
  const { data } = await api.get(`/stocks/${code}/price`, { params })
  return data
}

/** 取得最新一日基本資訊 */
export const fetchStockInfo = async (code) => {
  const { data } = await api.get(`/stocks/${code}/info`)
  return data
}

/** 取得三大法人買賣超 */
export const fetchInstitutional = async (code, start, end) => {
  const params = {}
  if (start) params.start = start
  if (end) params.end = end
  const { data } = await api.get(`/stocks/${code}/institutional`, { params })
  return data
}

/** 取得融資融券資訊 */
export const fetchMargin = async (code, start, end) => {
  const params = {}
  if (start) params.start = start
  if (end) params.end = end
  const { data } = await api.get(`/stocks/${code}/margin`, { params })
  return data
}
