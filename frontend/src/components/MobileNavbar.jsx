import React, {useState, useRef, useEffect} from 'react';
import { Menubar } from 'radix-ui';
import { HamburgerMenuIcon } from '@radix-ui/react-icons';
import Searchbar from './Searchbar';
import SearchResultsList from './SearchResultsList';


export default function MobileNavbar() {
  const [results, setResults] = useState([]);
  const [showResults, setShowResults] = useState(false);
  const searchRef = useRef(null);

  useEffect(() => {
    function handleClickOutside(event) {
      if (searchRef.current && !searchRef.current.contains(event.target)) {
        setShowResults(false);
      }
    }

  document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  return (
    <div className="min-w-full absolute left-0 right-0">
    <Menubar.Root className="visible md:invisible flex flex-start relative min-w-full left-0 right-0 border-b-1 border-[#D4D4D4] pb-5 px-6">
        <Menubar.Menu>
            <div className="flex flex-row-reverse gap-x-5">
            <h1 className="font-bold text-lg">Disaster Sentiment Tracker</h1>
            <Menubar.Trigger className="p-0 bg-white border-none"><HamburgerMenuIcon width="25" height="25"/></Menubar.Trigger>
            </div>
            <Menubar.Portal>
                <Menubar.Content
                    className="border border-[#D4D4D4] rounded-sm text-sm p-3 visible md:invisible mt-2 bg-white z-30"
                    align="start"
                    sideOffset={5}
                    alignOffset={-3}
                >

                <div ref = {searchRef} className="relative z-40">
                    {/* Search bar */}
                    <Searchbar
                        setResults={setResults}
                        onFocus={() => setShowResults(true)}
                    />
                    {showResults && 
                        <SearchResultsList 
                            results={results} 
                            onClickOutside={() => setShowResults(false)} 
                            onClickDisaster={() => setShowResults(false)} 
                        />
                    }
                </div>

                    <a className="text-sm text-black" href="/">
                        <Menubar.Item className="mt-3 py-1 hover:bg-[#F6F6F6] focus:outline-[1.5px] focus:outline-[#DFDFDF] rounded-sm">
                            <p className="pl-2">Most Recent</p>
                        </Menubar.Item>
                    </a>
                    <a className="text-sm text-black" href="/AllDisasters">
                        <Menubar.Item className="mt-2 py-1 hover:bg-[#F6F6F6] focus:outline-[1.5px] focus:outline-[#DFDFDF] rounded-sm">
                            <p className="pl-2">All Disasters</p>
                        </Menubar.Item>
                    </a>

                </Menubar.Content>
            </Menubar.Portal>
        </Menubar.Menu>
    </Menubar.Root>
    </div>
  );
}
