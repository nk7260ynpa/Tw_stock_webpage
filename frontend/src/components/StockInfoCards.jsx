import React from 'react'

function formatNumber(val) {
  if (val == null) return '--'
  return val.toLocaleString()
}

function formatPrice(val) {
  if (val == null) return '--'
  return val.toFixed(2)
}

export default function StockInfoCards({ info }) {
  if (!info) return null

  const isUp = info.change > 0
  const isDown = info.change < 0
  const changeColor = isUp ? 'text-red-600' : isDown ? 'text-green-600' : 'text-gray-600'
  const changeBg = isUp ? 'bg-red-50' : isDown ? 'bg-green-50' : 'bg-gray-50'
  const changeSign = isUp ? '+' : ''

  const cards = [
    {
      label: '收盤價',
      value: formatPrice(info.close),
      extra: info.change != null ? `${changeSign}${formatPrice(info.change)}` : null,
      color: changeColor,
      bg: changeBg,
    },
    {
      label: '開盤價',
      value: formatPrice(info.open),
    },
    {
      label: '最高價',
      value: formatPrice(info.high),
    },
    {
      label: '最低價',
      value: formatPrice(info.low),
    },
    {
      label: '成交量',
      value: formatNumber(info.volume),
      suffix: '股',
    },
    {
      label: '成交金額',
      value: formatNumber(info.trade_value),
      suffix: '元',
    },
    {
      label: '成交筆數',
      value: formatNumber(info.transaction),
    },
    {
      label: '本益比',
      value: info.pe_ratio != null ? info.pe_ratio.toFixed(2) : '--',
    },
  ]

  return (
    <div>
      <div className="flex items-baseline gap-3 mb-4">
        <h2 className="text-2xl font-bold">{info.code} {info.name}</h2>
        <span className={`text-sm px-2 py-0.5 rounded ${
          info.market === 'TWSE' ? 'bg-blue-100 text-blue-700' : 'bg-green-100 text-green-700'
        }`}>
          {info.market === 'TWSE' ? '上市' : '上櫃'}
        </span>
        <span className="text-sm text-gray-500">{info.date}</span>
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-8 gap-3">
        {cards.map((card) => (
          <div
            key={card.label}
            className={`rounded-lg p-3 ${card.bg || 'bg-white'} border border-gray-200`}
          >
            <div className="text-xs text-gray-500 mb-1">{card.label}</div>
            <div className={`text-lg font-semibold ${card.color || 'text-gray-900'}`}>
              {card.value}
              {card.suffix && <span className="text-xs font-normal text-gray-400 ml-1">{card.suffix}</span>}
            </div>
            {card.extra && (
              <div className={`text-sm ${card.color}`}>{card.extra}</div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}
