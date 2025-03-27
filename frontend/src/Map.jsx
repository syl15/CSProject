import React, { useEffect, useRef } from "react";
import L from "leaflet";
import "leaflet/dist/leaflet.css"; // Import Leaflet CSS

// need to run: npm install leaflet react-leaflet

export default function Map() {
  const mapRef = useRef(null); // Store map instance

  useEffect(() => {
    if (!mapRef.current) {
      // Ensure map initializes only once
      mapRef.current = L.map("map").setView([52.9857, -96.7502], 13);

      // Add a tile layer from OpenStreetMap
      L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: "&copy; OpenStreetMap contributors"
      }).addTo(mapRef.current);
    }

    return () => {
      if (mapRef.current) {
        mapRef.current.remove(); // Cleanup map instance
        mapRef.current = null; // Reset reference
      }
    };
  }, []);

  return (
    <div className="flex flex-col items-start border border-[#D4D4D4] rounded-md mt-4 text-left p-4">
      <h3> Location of Disaster</h3>
      <div id="map" className="w-full h-[500px]"></div>
    </div>
  );
}
