import React, { useEffect, useRef } from "react";
import L from "leaflet";
import "leaflet/dist/leaflet.css"; // Import Leaflet CSS

export default function Map() {
  const mapContainerRef = useRef(null); // Reference the div, not the map instance
  const mapInstanceRef = useRef(null); // Store the map instance separately

  useEffect(() => {
    if (!mapInstanceRef.current && mapContainerRef.current) {
      mapInstanceRef.current = L.map(mapContainerRef.current).setView([32.9857, -96.7502], 13); // Corrected UTD location

      L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: "&copy; OpenStreetMap contributors"
      }).addTo(mapInstanceRef.current);
    }

    return () => {
      if (mapInstanceRef.current) {
        mapInstanceRef.current.remove(); // Cleanup
        mapInstanceRef.current = null;
      }
    };
  }, []);

  return (
    <div className="flex flex-col border border-[#D4D4D4] rounded-md mt-4 text-left p-4">
        <div className="w-full border-b-1 border-[#D4D4D4]">
            <h3 className="pb-2">Location of Disaster</h3>
      </div>
      <div ref={mapContainerRef} className="w-[400px] h-[400px]"></div>
    </div>
  );
}


// need to run: npm install leaflet react-leaflet