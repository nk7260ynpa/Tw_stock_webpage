import React from 'react'
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
  ReferenceLine,
} from 'recharts'

export default function InstitutionalInfo({ data }) {
  if (!data || !data.records || data.records.length === 0) return null

  const chartData = data.records.map((r) => ({
    date: r.date,
    foreign: r.foreign_buy_sell,
    trust: r.investment_trust_buy_sell,
    dealer: r.dealer_buy_sell,
    total: r.total_buy_sell,
  }))

  return (
    <div className="bg-white rounded-lg border border-gray-200 p-4">
      <h3 className="font-semibold text-gray-700 mb-4">三大法人買賣超</h3>

      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={chartData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
          <XAxis dataKey="date" tick={{ fontSize: 11 }} tickFormatter={(v) => v.slice(5)} />
          <YAxis
            tick={{ fontSize: 11 }}
            tickFormatter={(val) => {
              if (Math.abs(val) >= 1e8) return `${(val / 1e8).toFixed(0)}億`
              if (Math.abs(val) >= 1e4) return `${(val / 1e4).toFixed(0)}萬`
              return val
            }}
          />
          <Tooltip
            formatter={(val, name) => {
              const labels = {
                foreign: '外資',
                trust: '投信',
                dealer: '自營商',
                total: '合計',
              }
              return [val?.toLocaleString(), labels[name] || name]
            }}
            labelFormatter={(label) => `日期: ${label}`}
          />
          <Legend
            formatter={(val) => {
              const labels = { foreign: '外資', trust: '投信', dealer: '自營商' }
              return labels[val] || val
            }}
          />
          <ReferenceLine y={0} stroke="#9ca3af" />
          <Bar dataKey="foreign" fill="#3b82f6" barSize={8} />
          <Bar dataKey="trust" fill="#22c55e" barSize={8} />
          <Bar dataKey="dealer" fill="#f59e0b" barSize={8} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}
