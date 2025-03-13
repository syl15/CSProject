import React from 'react'
import { MagnifyingGlassIcon } from '@radix-ui/react-icons'

export default function Searchbar() {
  return (
    <div className="relative">
        <MagnifyingGlassIcon className="absolute left-3 top-[11px]"/>
        <input
            className="h-[38px] pl-8 pr-2 border border-[#D4D4D4] rounded-sm text-sm focus:outline-0"
            type="text"
            id="keyword"
            placeholder="Search"
        />
    </div>
  )
}
