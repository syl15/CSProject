import React from 'react';
import { NavigationMenu, Menubar } from 'radix-ui';
import Searchbar from './Searchbar';
import './Navbar.css'
import { HamburgerMenuIcon } from '@radix-ui/react-icons';
import MobileNavbar from './MobileNavbar';

export default function Navbar() {
  return (
    <div className="overflow-x-hidden absolute left-0 right-0 md:border-b-1 md:border-[#D4D4D4] pb-5 px-6 md:px-10">
        <MobileNavbar/>
        <NavigationMenu.Root className="invisible md:visible flex flex-row justify-between items-between">
            <div className="flex flex-row items-center gap-x-10">
                <h1 className="font-bold text-lg">Disaster Sentiment Tracker</h1>
                <NavigationMenu.List className="flex flex-row gap-x-2">
                    {/* Overview */}
                    <NavigationMenu.Link className="text-sm" href="https://github.com/radix-ui">
                        <NavigationMenu.Item className="list-none nav-item">
                            Overview
                        </NavigationMenu.Item>
                    </NavigationMenu.Link>

                    {/* Past Disasters */}
                    <NavigationMenu.Link className="text-sm" href="https://github.com/radix-ui">
                        <NavigationMenu.Item className="list-none nav-item">
                            Past Disasters
                        </NavigationMenu.Item>
                    </NavigationMenu.Link>
                </NavigationMenu.List>
            </div>
            {/* Search bar */}
            <Searchbar />
	    </NavigationMenu.Root>
   
    </div>
    
  );
}