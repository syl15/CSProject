import React from 'react'
import { Menubar } from 'radix-ui';
import { HamburgerMenuIcon } from '@radix-ui/react-icons';
import Searchbar from './Searchbar';


export default function MobileNavbar() {
  return (
    <Menubar.Root className="visible md:invisible flex flex-start absolute w-screen left-0 right-0 border-b-1 border-[#D4D4D4] pb-5 px-6">
        <Menubar.Menu>
            <div className="flex flex-row-reverse gap-x-5">
            <h1 className="font-bold text-lg">Disaster Sentiment Tracker</h1>
            <Menubar.Trigger className="p-0 bg-white border-none"><HamburgerMenuIcon width="25" height="25"/></Menubar.Trigger>
            </div>
            <Menubar.Portal>
                <Menubar.Content
                    className="border border-[#D4D4D4] rounded-sm text-sm p-3 visible md:invisible mt-2 bg-white"
                    align="start"
                    sideOffset={5}
                    alignOffset={-3}
                >
                    <Searchbar />
                    <a className="text-sm text-black" href="https://github.com/radix-ui">
                        <Menubar.Item className="mt-3 py-1 hover:bg-[#F6F6F6] focus:outline-[1.5px] focus:outline-[#DFDFDF] rounded-sm">
                            <p className="pl-2">Overview</p>
                        </Menubar.Item>
                    </a>
                    <a className="text-sm text-black" href="https://github.com/radix-ui">
                        <Menubar.Item className="mt-2 py-1 hover:bg-[#F6F6F6] focus:outline-[1.5px] focus:outline-[#DFDFDF] rounded-sm">
                            <p className="pl-2">All Disasters</p>
                        </Menubar.Item>
                    </a>

                </Menubar.Content>
            </Menubar.Portal>
        </Menubar.Menu>
    </Menubar.Root>
  );
}
