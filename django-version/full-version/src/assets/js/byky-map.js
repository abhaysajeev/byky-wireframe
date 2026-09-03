/**
 * BYKY station map
 *
 * Shared Leaflet/OpenStreetMap map used on operational screens (fleet registry,
 * station address mapping). Marker radius tracks the fleet held at each station.
 * Points are supplied by the server via #byky-map-data.
 */

'use strict';

(function () {
  const el = document.getElementById('stationMap');
  const src = document.getElementById('byky-map-data');
  if (!el || !src || typeof L === 'undefined') return;

  const points = JSON.parse(src.textContent);
  if (!points.length) return;

  const primary = config.colors.primary;
  const map = L.map(el, { scrollWheelZoom: false }).setView([24.9, 55.4], 7);

  // Basemap: Esri light-gray canvas plus its reference (label) layer.
  //
  // Chosen over OSM's standard tiles because those render place names in the local
  // script -- Arabic across the UAE -- and this dashboard is read in English. Esri's
  // canvas labels are latin. The neutral grey base also keeps the red station
  // markers the loudest thing on the map.
  //
  // Tile servers require a Referer; Django's default SECURE_REFERRER_POLICY of
  // "same-origin" strips it, so settings.py sets "strict-origin-when-cross-origin".
  const esri = 'https://server.arcgisonline.com/ArcGIS/rest/services';
  L.tileLayer(esri + '/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}', {
    attribution: 'Tiles &copy; Esri &mdash; &copy; OpenStreetMap contributors',
    maxZoom: 16
  }).addTo(map);
  L.tileLayer(esri + '/Canvas/World_Light_Gray_Reference/MapServer/tile/{z}/{y}/{x}', {
    maxZoom: 16,
    pane: 'overlayPane'
  }).addTo(map);

  const maxFleet = Math.max.apply(null, points.map(p => p.fleet)) || 1;

  const markers = points.map(p => {
    const radius = p.fleet ? 6 + Math.round((p.fleet / maxFleet) * 14) : 5;
    return L.circleMarker([p.lat, p.lng], {
      radius,
      color: primary,
      weight: 2,
      fillColor: primary,
      fillOpacity: p.fleet ? 0.45 : 0.12
    })
      .bindPopup(
        `<div style="min-width:160px">
           <div style="font-weight:600;margin-bottom:2px">${p.name}</div>
           <div style="opacity:.7;margin-bottom:6px">${p.emirate}</div>
           <div><strong>${p.fleet}</strong> vehicles</div>
         </div>`
      )
      .addTo(map);
  });

  // Frame the UAE cluster; the lone Kuwait station stays plotted but would
  // otherwise pull the view out to the whole Gulf.
  const core = markers.filter((m, i) => points[i].emirate !== 'Kuwait');
  map.fitBounds(L.featureGroup(core.length ? core : markers).getBounds().pad(0.12));
  setTimeout(() => map.invalidateSize(), 250);
})();
