import React, { useState, useRef, useEffect } from 'react'

export default function StockSelector({ stocks, onSelect }) {
  const [query, setQuery] = useState('')
  const [isOpen, setIsOpen] = useState(false)
  const wrapperRef = useRef(null)

  // 點擊外部關閉下拉選單
  useEffect(() => {
    const handleClickOutside = (e) => {
      if (wrapperRef.current && !wrapperRef.current.contains(e.target)) {
        setIsOpen(false)
      }
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  const filtered = stocks.filter((s) => {
    const q = query.trim().toLowerCase()
    if (!q) return true
    return s.code.toLowerCase().includes(q) || s.name.toLowerCase().includes(q)
  }).slice(0, 50) // 限制顯示數量

  const handleSelect = (stock) => {
    setQuery(`${stock.code} ${stock.name}`)
    setIsOpen(false)
    onSelect(stock.code)
  }

  return (
    <div ref={wrapperRef} className="relative flex-1 max-w-md">
      <input
        type="text"
        value={query}
        onChange={(e) => {
          setQuery(e.target.value)
          setIsOpen(true)
        }}
        onFocus={() => setIsOpen(true)}
        placeholder="搜尋股票代號或名稱..."
        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
      />
      {isOpen && filtered.length > 0 && (
        <ul className="absolute z-50 w-full mt-1 bg-white border border-gray-200 rounded-lg shadow-lg max-h-80 overflow-y-auto">
          {filtered.map((stock) => (
            <li
              key={`${stock.market}-${stock.code}`}
              onClick={() => handleSelect(stock)}
              className="px-4 py-2 cursor-pointer hover:bg-blue-50 flex justify-between items-center"
            >
              <span>
                <span className="font-medium">{stock.code}</span>
                <span className="ml-2 text-gray-600">{stock.name}</span>
              </span>
              <span className={`text-xs px-2 py-0.5 rounded ${
                stock.market === 'TWSE'
                  ? 'bg-blue-100 text-blue-700'
                  : 'bg-green-100 text-green-700'
              }`}>
                {stock.market === 'TWSE' ? '上市' : '上櫃'}
              </span>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
