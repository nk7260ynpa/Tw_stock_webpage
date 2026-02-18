import React from 'react'
import {
  ComposedChart,
  Line,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from 'recharts'

export default function MarginInfo({ data }) {
  if (!data || !data.records || data.records.length === 0) return null

  const chartData = data.records.map((r) => ({
    date: r.date,
    margin_balance: r.margin_balance,
    short_balance: r.short_balance,
    margin_purchase: r.margin_purchase,
    margin_sales: r.margin_sales,
    short_sale: r.short_sale,
    short_covering: r.short_covering,
  }))

  return (
    <div className="bg-white rounded-lg border border-gray-200 p-4">
      <h3 className="font-semibold text-gray-700 mb-4">融資融券</h3>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {/* 融資餘額 */}
        <div>
          <h4 className="text-sm text-gray-500 mb-2">融資餘額</h4>
          <ResponsiveContainer width="100%" height={250}>
            <ComposedChart data={chartData} margin={{ top: 10, right: 20, left: 0, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis dataKey="date" tick={{ fontSize: 10 }} tickFormatter={(v) => v.slice(5)} />
              <YAxis tick={{ fontSize: 10 }} tickFormatter={(v) => v >= 1000 ? `${(v / 1000).toFixed(0)}K` : v} />
              <Tooltip
                formatter={(val, name) => {
                  const labels = {
                    margin_balance: '融資餘額',
                    margin_purchase: '融資買進',
                    margin_sales: '融資賣出',
                  }
                  return [val?.toLocaleString(), labels[name] || name]
                }}
                labelFormatter={(label) => `日期: ${label}`}
              />
              <Legend
                formatter={(val) => {
                  const labels = {
                    margin_balance: '融資餘額',
                    margin_purchase: '融資買進',
                    margin_sales: '融資賣出',
                  }
                  return labels[val] || val
                }}
              />
              <Bar dataKey="margin_purchase" fill="#ef4444" barSize={4} opacity={0.7} />
              <Bar dataKey="margin_sales" fill="#22c55e" barSize={4} opacity={0.7} />
              <Line type="monotone" dataKey="margin_balance" stroke="#3b82f6" dot={false} strokeWidth={2} connectNulls />
            </ComposedChart>
          </ResponsiveContainer>
        </div>

        {/* 融券餘額 */}
        <div>
          <h4 className="text-sm text-gray-500 mb-2">融券餘額</h4>
          <ResponsiveContainer width="100%" height={250}>
            <ComposedChart data={chartData} margin={{ top: 10, right: 20, left: 0, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis dataKey="date" tick={{ fontSize: 10 }} tickFormatter={(v) => v.slice(5)} />
              <YAxis tick={{ fontSize: 10 }} tickFormatter={(v) => v >= 1000 ? `${(v / 1000).toFixed(0)}K` : v} />
              <Tooltip
                formatter={(val, name) => {
                  const labels = {
                    short_balance: '融券餘額',
                    short_sale: '融券賣出',
                    short_covering: '融券回補',
                  }
                  return [val?.toLocaleString(), labels[name] || name]
                }}
                labelFormatter={(label) => `日期: ${label}`}
              />
              <Legend
                formatter={(val) => {
                  const labels = {
                    short_balance: '融券餘額',
                    short_sale: '融券賣出',
                    short_covering: '融券回補',
                  }
                  return labels[val] || val
                }}
              />
              <Bar dataKey="short_sale" fill="#f59e0b" barSize={4} opacity={0.7} />
              <Bar dataKey="short_covering" fill="#8b5cf6" barSize={4} opacity={0.7} />
              <Line type="monotone" dataKey="short_balance" stroke="#ef4444" dot={false} strokeWidth={2} connectNulls />
            </ComposedChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  )
}
