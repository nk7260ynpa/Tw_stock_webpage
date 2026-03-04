import React, { useState, useEffect, useCallback } from 'react'
import StockSelector from './components/StockSelector'
import StockInfoCards from './components/StockInfoCards'
import CandlestickChart from './components/CandlestickChart'
import IndicatorChart from './components/IndicatorChart'
import InstitutionalInfo from './components/InstitutionalInfo'
import MarginInfo from './components/MarginInfo'
import {
  fetchStocks,
  fetchPriceHistory,
  fetchStockInfo,
  fetchInstitutional,
  fetchMargin,
} from './api/stock'

export default function App() {
  const [stocks, setStocks] = useState([])
  const [selectedCode, setSelectedCode] = useState(null)
  const [stockInfo, setStockInfo] = useState(null)
  const [priceData, setPriceData] = useState(null)
  const [institutionalData, setInstitutionalData] = useState(null)
  const [marginData, setMarginData] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  // 載入股票清單
  useEffect(() => {
    fetchStocks()
      .then(setStocks)
      .catch((err) => setError('無法載入股票清單: ' + err.message))
  }, [])

  // 從 URL 查詢參數自動選股（例如 ?code=2330）
  useEffect(() => {
    if (stocks.length > 0 && !selectedCode) {
      const params = new URLSearchParams(window.location.search)
      const code = params.get('code')
      if (code) {
        handleSelect(code)
      }
    }
  }, [stocks])

  // 選擇股票後載入所有資料
  const handleSelect = useCallback(async (code) => {
    setSelectedCode(code)
    setLoading(true)
    setError(null)

    try {
      const results = await Promise.allSettled([
        fetchStockInfo(code),
        fetchPriceHistory(code),
        fetchInstitutional(code),
        fetchMargin(code),
      ])

      const [infoResult, priceResult, institutionalResult, marginResult] = results

      // 基本資訊與股價為必要資料
      if (infoResult.status === 'fulfilled') {
        setStockInfo(infoResult.value)
      } else {
        setError('載入基本資訊失敗: ' + infoResult.reason?.message)
      }

      if (priceResult.status === 'fulfilled') {
        setPriceData(priceResult.value)
      }

      // 三大法人與融資融券為輔助資料，失敗不影響主要顯示
      if (institutionalResult.status === 'fulfilled') {
        setInstitutionalData(institutionalResult.value)
      }

      if (marginResult.status === 'fulfilled') {
        setMarginData(marginResult.value)
      }
    } catch (err) {
      setError('載入資料失敗: ' + err.message)
    } finally {
      setLoading(false)
    }
  }, [])

  return (
    <div className="min-h-screen bg-gray-50">
      {/* 頂部導覽列 */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 py-3 flex items-center gap-4">
          <h1 className="text-xl font-bold text-gray-800 whitespace-nowrap">
            台灣股票資訊
          </h1>
          <StockSelector stocks={stocks} onSelect={handleSelect} />
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-6 space-y-6">
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
            {error}
          </div>
        )}

        {loading && (
          <div className="flex justify-center py-20">
            <div className="animate-spin rounded-full h-12 w-12 border-4 border-blue-500 border-t-transparent" />
          </div>
        )}

        {!loading && stockInfo && (
          <>
            <StockInfoCards info={stockInfo} />

            {priceData && priceData.prices.length > 0 && (
              <>
                <CandlestickChart
                  prices={priceData.prices}
                  indicators={priceData.indicators}
                />
                <IndicatorChart
                  indicators={priceData.indicators}
                />
              </>
            )}

            {institutionalData && institutionalData.records.length > 0 && (
              <InstitutionalInfo data={institutionalData} />
            )}

            {marginData && marginData.records.length > 0 && (
              <MarginInfo data={marginData} />
            )}
          </>
        )}

        {!loading && !selectedCode && (
          <div className="text-center py-20 text-gray-400">
            <p className="text-lg">請選擇股票以查看詳細資訊</p>
          </div>
        )}
      </main>
    </div>
  )
}
