import React, { useState } from 'react'
import {
  ComposedChart,
  Line,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  ReferenceLine,
} from 'recharts'

const TABS = [
  { key: 'rsi', label: 'RSI' },
  { key: 'macd', label: 'MACD' },
  { key: 'kd', label: 'KD' },
]

function RSIChart({ data }) {
  return (
    <ResponsiveContainer width="100%" height={200}>
      <ComposedChart data={data} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
        <XAxis dataKey="date" tick={{ fontSize: 11 }} tickFormatter={(v) => v.slice(5)} />
        <YAxis domain={[0, 100]} tick={{ fontSize: 11 }} />
        <Tooltip
          formatter={(val) => val?.toFixed(2)}
          labelFormatter={(label) => `日期: ${label}`}
        />
        <ReferenceLine y={70} stroke="#ef4444" strokeDasharray="3 3" label={{ value: '70', position: 'right', fontSize: 10 }} />
        <ReferenceLine y={30} stroke="#22c55e" strokeDasharray="3 3" label={{ value: '30', position: 'right', fontSize: 10 }} />
        <Line type="monotone" dataKey="rsi" stroke="#8b5cf6" dot={false} strokeWidth={2} connectNulls name="RSI" />
      </ComposedChart>
    </ResponsiveContainer>
  )
}

function MACDChart({ data }) {
  return (
    <ResponsiveContainer width="100%" height={200}>
      <ComposedChart data={data} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
        <XAxis dataKey="date" tick={{ fontSize: 11 }} tickFormatter={(v) => v.slice(5)} />
        <YAxis tick={{ fontSize: 11 }} />
        <Tooltip
          formatter={(val) => val?.toFixed(2)}
          labelFormatter={(label) => `日期: ${label}`}
        />
        <ReferenceLine y={0} stroke="#9ca3af" />
        <Bar
          dataKey="macd_hist"
          name="柱狀圖"
          barSize={4}
          fill="#94a3b8"
          shape={(props) => {
            const { x, y, width, height, value } = props
            return (
              <rect
                x={x}
                y={y}
                width={width}
                height={Math.abs(height)}
                fill={value >= 0 ? '#ef4444' : '#22c55e'}
              />
            )
          }}
        />
        <Line type="monotone" dataKey="macd" stroke="#3b82f6" dot={false} strokeWidth={1.5} connectNulls name="MACD" />
        <Line type="monotone" dataKey="macd_signal" stroke="#f59e0b" dot={false} strokeWidth={1.5} connectNulls name="Signal" />
      </ComposedChart>
    </ResponsiveContainer>
  )
}

function KDChart({ data }) {
  return (
    <ResponsiveContainer width="100%" height={200}>
      <ComposedChart data={data} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
        <XAxis dataKey="date" tick={{ fontSize: 11 }} tickFormatter={(v) => v.slice(5)} />
        <YAxis domain={[0, 100]} tick={{ fontSize: 11 }} />
        <Tooltip
          formatter={(val) => val?.toFixed(2)}
          labelFormatter={(label) => `日期: ${label}`}
        />
        <ReferenceLine y={80} stroke="#ef4444" strokeDasharray="3 3" label={{ value: '80', position: 'right', fontSize: 10 }} />
        <ReferenceLine y={20} stroke="#22c55e" strokeDasharray="3 3" label={{ value: '20', position: 'right', fontSize: 10 }} />
        <Line type="monotone" dataKey="k" stroke="#3b82f6" dot={false} strokeWidth={2} connectNulls name="K" />
        <Line type="monotone" dataKey="d" stroke="#f59e0b" dot={false} strokeWidth={2} connectNulls name="D" />
      </ComposedChart>
    </ResponsiveContainer>
  )
}

export default function IndicatorChart({ indicators }) {
  const [activeTab, setActiveTab] = useState('rsi')

  if (!indicators || indicators.length === 0) return null

  return (
    <div className="bg-white rounded-lg border border-gray-200 p-4">
      <div className="flex items-center gap-4 mb-4">
        <h3 className="font-semibold text-gray-700">技術指標</h3>
        <div className="flex gap-1">
          {TABS.map((tab) => (
            <button
              key={tab.key}
              onClick={() => setActiveTab(tab.key)}
              className={`px-3 py-1 text-sm rounded ${
                activeTab === tab.key
                  ? 'bg-blue-500 text-white'
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>
      </div>

      {activeTab === 'rsi' && <RSIChart data={indicators} />}
      {activeTab === 'macd' && <MACDChart data={indicators} />}
      {activeTab === 'kd' && <KDChart data={indicators} />}
    </div>
  )
}
