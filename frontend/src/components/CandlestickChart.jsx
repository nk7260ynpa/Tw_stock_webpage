import React, { useState } from 'react'
import {
  ComposedChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Line,
  ReferenceLine,
} from 'recharts'

/** 自訂 K 線蠟燭形狀 */
const CandlestickShape = (props) => {
  const { x, y, width, height, payload } = props
  if (!payload) return null

  const { open, close, high, low } = payload
  if (open == null || close == null || high == null || low == null) return null

  const isUp = close >= open
  const color = isUp ? '#ef4444' : '#22c55e'
  const bodyTop = Math.min(open, close)
  const bodyBottom = Math.max(open, close)

  // 價格範圍（從 YAxis domain 推算）
  const chartArea = props.background || {}
  const areaHeight = chartArea.height || height
  const areaY = chartArea.y || y

  // 使用 Bar 的座標系統
  const midX = x + width / 2

  return (
    <g>
      {/* 上影線 */}
      <line
        x1={midX}
        y1={props.yAxisMap ? props.yAxisMap(high) : y}
        x2={midX}
        y2={props.yAxisMap ? props.yAxisMap(bodyBottom) : y}
        stroke={color}
        strokeWidth={1}
      />
      {/* 實體 */}
      <rect
        x={x + 1}
        y={y}
        width={Math.max(width - 2, 1)}
        height={Math.max(Math.abs(height), 1)}
        fill={isUp ? color : color}
        stroke={color}
      />
      {/* 下影線 */}
      <line
        x1={midX}
        y1={props.yAxisMap ? props.yAxisMap(bodyTop) : y + Math.abs(height)}
        x2={midX}
        y2={props.yAxisMap ? props.yAxisMap(low) : y + Math.abs(height)}
        stroke={color}
        strokeWidth={1}
      />
    </g>
  )
}

/** 自訂 Tooltip */
const CustomTooltip = ({ active, payload }) => {
  if (!active || !payload || !payload.length) return null
  const data = payload[0]?.payload
  if (!data) return null

  const isUp = (data.close ?? 0) >= (data.open ?? 0)
  const color = isUp ? 'text-red-600' : 'text-green-600'

  return (
    <div className="bg-white border border-gray-200 rounded-lg shadow-lg p-3 text-sm">
      <div className="font-medium mb-1">{data.date}</div>
      <div className="grid grid-cols-2 gap-x-4 gap-y-1">
        <span className="text-gray-500">開盤</span>
        <span className={color}>{data.open?.toFixed(2)}</span>
        <span className="text-gray-500">最高</span>
        <span className={color}>{data.high?.toFixed(2)}</span>
        <span className="text-gray-500">最低</span>
        <span className={color}>{data.low?.toFixed(2)}</span>
        <span className="text-gray-500">收盤</span>
        <span className={color}>{data.close?.toFixed(2)}</span>
        <span className="text-gray-500">漲跌</span>
        <span className={color}>{data.change?.toFixed(2)}</span>
        <span className="text-gray-500">成交量</span>
        <span>{data.volume?.toLocaleString()}</span>
      </div>
    </div>
  )
}

const MA_COLORS = {
  ma5: '#f59e0b',
  ma10: '#3b82f6',
  ma20: '#ef4444',
  ma60: '#8b5cf6',
}

export default function CandlestickChart({ prices, indicators }) {
  const [showMA, setShowMA] = useState({ ma5: true, ma10: true, ma20: true, ma60: false })
  const [showBB, setShowBB] = useState(false)

  // 合併價格與指標資料
  const chartData = prices.map((p, i) => ({
    ...p,
    ...(indicators[i] || {}),
    // 用於 bar chart 的漲跌色
    volumeColor: (p.close ?? 0) >= (p.open ?? 0) ? '#ef4444' : '#22c55e',
  }))

  // 計算 Y 軸範圍
  const validPrices = prices.filter((p) => p.low != null && p.high != null)
  const minPrice = Math.min(...validPrices.map((p) => p.low))
  const maxPrice = Math.max(...validPrices.map((p) => p.high))
  const priceMargin = (maxPrice - minPrice) * 0.05
  const maxVolume = Math.max(...prices.map((p) => p.volume || 0))

  return (
    <div className="bg-white rounded-lg border border-gray-200 p-4">
      <div className="flex items-center gap-4 mb-4">
        <h3 className="font-semibold text-gray-700">K 線圖</h3>
        <div className="flex gap-2 text-sm">
          {Object.entries(MA_COLORS).map(([key, color]) => (
            <label key={key} className="flex items-center gap-1 cursor-pointer">
              <input
                type="checkbox"
                checked={showMA[key]}
                onChange={() => setShowMA((prev) => ({ ...prev, [key]: !prev[key] }))}
                className="rounded"
              />
              <span style={{ color }}>{key.toUpperCase()}</span>
            </label>
          ))}
          <label className="flex items-center gap-1 cursor-pointer">
            <input
              type="checkbox"
              checked={showBB}
              onChange={() => setShowBB(!showBB)}
              className="rounded"
            />
            <span className="text-gray-600">布林通道</span>
          </label>
        </div>
      </div>

      {/* K 線主圖 */}
      <ResponsiveContainer width="100%" height={400}>
        <ComposedChart data={chartData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
          <XAxis
            dataKey="date"
            tick={{ fontSize: 11 }}
            tickFormatter={(val) => val.slice(5)}
          />
          <YAxis
            yAxisId="price"
            domain={[minPrice - priceMargin, maxPrice + priceMargin]}
            tick={{ fontSize: 11 }}
            tickFormatter={(val) => val.toFixed(0)}
          />
          <YAxis
            yAxisId="volume"
            orientation="right"
            domain={[0, maxVolume * 4]}
            tick={{ fontSize: 11 }}
            tickFormatter={(val) => val >= 1e8 ? `${(val / 1e8).toFixed(0)}億` : val >= 1e4 ? `${(val / 1e4).toFixed(0)}萬` : val}
            hide
          />
          <Tooltip content={<CustomTooltip />} />

          {/* 成交量 */}
          <Bar
            yAxisId="volume"
            dataKey="volume"
            fill="#d1d5db"
            opacity={0.5}
            barSize={6}
          />

          {/* K 線 (用兩條線模擬) */}
          <Line yAxisId="price" type="monotone" dataKey="high" stroke="transparent" dot={false} />
          <Line yAxisId="price" type="monotone" dataKey="low" stroke="transparent" dot={false} />

          {/* 收盤價線（作為 K 線的替代顯示） */}
          <Bar
            yAxisId="price"
            dataKey="close"
            barSize={6}
            shape={(props) => {
              const { x, width, payload } = props
              if (!payload || payload.open == null || payload.close == null) return null

              const { open, close, high, low } = payload
              const isUp = close >= open

              const color = isUp ? '#ef4444' : '#22c55e'
              const midX = x + width / 2

              // 從 YAxis 取得座標
              const yScale = props.y !== undefined ? (val) => {
                const domain = [minPrice - priceMargin, maxPrice + priceMargin]
                const range = [400 - 30, 10]  // 預估圖表區域
                return range[0] + (range[1] - range[0]) * ((val - domain[0]) / (domain[1] - domain[0]))
              } : null

              if (!yScale) return null

              const yHigh = yScale(high)
              const yLow = yScale(low)
              const yOpen = yScale(open)
              const yClose = yScale(close)
              const yBodyTop = Math.min(yOpen, yClose)
              const yBodyBottom = Math.max(yOpen, yClose)

              return (
                <g>
                  <line x1={midX} y1={yHigh} x2={midX} y2={yBodyTop} stroke={color} strokeWidth={1} />
                  <rect
                    x={x + 1}
                    y={yBodyTop}
                    width={Math.max(width - 2, 2)}
                    height={Math.max(yBodyBottom - yBodyTop, 1)}
                    fill={isUp ? 'none' : color}
                    stroke={color}
                    strokeWidth={1}
                  />
                  <line x1={midX} y1={yBodyBottom} x2={midX} y2={yLow} stroke={color} strokeWidth={1} />
                </g>
              )
            }}
          />

          {/* 均線 */}
          {Object.entries(MA_COLORS).map(([key, color]) =>
            showMA[key] && (
              <Line
                key={key}
                yAxisId="price"
                type="monotone"
                dataKey={key}
                stroke={color}
                dot={false}
                strokeWidth={1.5}
                connectNulls
              />
            )
          )}

          {/* 布林通道 */}
          {showBB && (
            <>
              <Line yAxisId="price" type="monotone" dataKey="bb_upper" stroke="#9ca3af" dot={false} strokeDasharray="4 2" connectNulls />
              <Line yAxisId="price" type="monotone" dataKey="bb_middle" stroke="#6b7280" dot={false} strokeDasharray="4 2" connectNulls />
              <Line yAxisId="price" type="monotone" dataKey="bb_lower" stroke="#9ca3af" dot={false} strokeDasharray="4 2" connectNulls />
            </>
          )}
        </ComposedChart>
      </ResponsiveContainer>
    </div>
  )
}
