import React from 'react'
import Navbar from './components/Navbar'
import DisasterCard from './components/DisasterCard'
import FilterColumn from './components/FilterColumn'

export default function AllDisasters() {
  return (
    <div className="flex flex-col mt-30 w-screen min-h-screen h-auto absolute left-0 right-0 px-10 md:px-20 pb-10 overflow-x-hidden">
        <h1 className="text-4xl font-bold text-left">All Disasters</h1>
        <div className="flex flex-col gap-y-10 md:flex-row">
            <FilterColumn/>
            <DisasterCard/>
        </div>

        
    </div>
  )
}