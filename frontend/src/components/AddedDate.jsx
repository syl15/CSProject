import React from 'react'


export default function AddedDate({dateAdded}) {
  return (
    <div className="flex flex-col flex-start border border-[#D4D4D4] rounded-md mt-5 md:mt-15 text-left p-4 gap-y-2">
        <h3>Date Added</h3>
        <h1 className="text-3xl font-bold">{dateAdded}</h1>
    </div>
  );
}
