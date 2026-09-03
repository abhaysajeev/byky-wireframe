/**
 * BYKY Dashboard
 *
 * Charts and the station network map. Every series is supplied by the server
 * through the #byky-chart-data JSON tag; nothing is hardcoded here.
 *
 * Fleet and station series come from BYKY's own records. Revenue series are
 * indicative, generated in apps/byky_core/sales.py, and the cards that show them
 * are labelled as such.
 */

'use strict';

(function () {
  const dataEl = document.getElementById('byky-chart-data');
  if (!dataEl) return;
  const data = JSON.parse(dataEl.textContent);

  const cardColor = config.colors.cardColor;
  const labelColor = config.colors.textMuted;
  const headingColor = config.colors.headingColor;
  const fontFamily = config.fontFamily;
  const primary = config.colors.primary;
  const borderColor = config.colors.borderColor;

  const aed = v => 'AED ' + Number(v).toLocaleString();

  // Swiper: revenue / fleet / network
  // --------------------------------------------------------------------
  const swiperEl = document.querySelector('#swiper-with-pagination-cards');
  if (swiperEl) {
    new Swiper(swiperEl, {
      loop: true,
      // No autoplay. On a card this dense any mid-transition frame shows two
      // slides at once, which reads as overlapping text -- and a dashboard that
      // animates by itself is a distraction during a walkthrough. The pagination
      // dots stay clickable, so all three views are still reachable.
      effect: 'fade',
      fadeEffect: { crossFade: false },
      speed: 300,
      pagination: { clickable: true, el: '.swiper-pagination' }
    });
  }

  // Average Daily Sales -- 30-day revenue curve
  // --------------------------------------------------------------------
  const dailyEl = document.querySelector('#dailySales');
  if (dailyEl) {
    new ApexCharts(dailyEl, {
      chart: {
        height: 150, type: 'area', parentHeightOffset: 0,
        toolbar: { show: false }, sparkline: { enabled: true }
      },
      markers: { colors: 'transparent', strokeColors: 'transparent' },
      grid: { show: false },
      colors: [primary],
      fill: {
        type: 'gradient',
        gradient: { shade: 'light', shadeIntensity: 0.8, opacityFrom: 0.6, opacityTo: 0.1, stops: [0, 95, 100] }
      },
      dataLabels: { enabled: false },
      stroke: { width: 2, curve: 'smooth' },
      series: [{ name: 'Revenue', data: data.daily_revenue }],
      xaxis: { categories: data.daily_labels, show: false, labels: { show: false }, axisBorder: { show: false } },
      yaxis: { show: false },
      tooltip: {
        enabled: true,
        x: { show: true },
        y: { formatter: aed, title: { formatter: () => 'Revenue' } }
      }
    }).render();
  }

  // Revenue Reports -- 12 months
  // --------------------------------------------------------------------
  const revenueEl = document.querySelector('#revenueReports');
  if (revenueEl) {
    new ApexCharts(revenueEl, {
      chart: { height: 200, parentHeightOffset: 0, type: 'bar', toolbar: { show: false } },
      plotOptions: { bar: { barHeight: '60%', columnWidth: '58%', borderRadius: 5, distributed: true } },
      grid: { show: false, padding: { top: -20, bottom: 0, left: -10, right: -10 } },
      colors: [primary],
      dataLabels: { enabled: false },
      legend: { show: false },
      series: [{ name: 'Revenue', data: data.monthly_revenue }],
      xaxis: {
        categories: data.monthly_labels,
        axisBorder: { show: false }, axisTicks: { show: false },
        labels: { style: { colors: labelColor, fontFamily, fontSize: '11px' } }
      },
      yaxis: { labels: { show: false } },
      tooltip: { y: { formatter: aed } },
      states: { hover: { filter: { type: 'none' } } }
    }).render();
  }

  // Fleet Deployment gauge
  // --------------------------------------------------------------------
  const deploymentEl = document.querySelector('#deploymentStatus');
  if (deploymentEl) {
    new ApexCharts(deploymentEl, {
      series: [data.deployment_pct],
      labels: ['Stocked'],
      chart: { height: 340, type: 'radialBar' },
      plotOptions: {
        radialBar: {
          offsetY: 10, startAngle: -140, endAngle: 130,
          hollow: { size: '65%' },
          track: { background: cardColor, strokeWidth: '100%' },
          dataLabels: {
            name: { offsetY: -20, color: labelColor, fontFamily, fontSize: '13px', fontWeight: '400' },
            value: { offsetY: 10, color: headingColor, fontFamily, fontSize: '38px', fontWeight: '500', formatter: v => v + '%' }
          }
        }
      },
      colors: [primary],
      fill: {
        type: 'gradient',
        gradient: {
          shade: 'dark', shadeIntensity: 0.5, gradientToColors: [primary],
          inverseColors: true, opacityFrom: 1, opacityTo: 0.6, stops: [30, 70, 100]
        }
      },
      stroke: { dashArray: 10 },
      grid: { padding: { top: -20, bottom: -20 } },
      states: { hover: { filter: { type: 'none' } } }
    }).render();
  }

  // Revenue by Category
  // --------------------------------------------------------------------
  const categoryEl = document.querySelector('#revenueByCategory');
  if (categoryEl) {
    new ApexCharts(categoryEl, {
      chart: { height: 270, parentHeightOffset: 0, type: 'bar', toolbar: { show: false } },
      plotOptions: { bar: { horizontal: true, barHeight: '70%', borderRadius: 4 } },
      grid: {
        borderColor, strokeDashArray: 6,
        xaxis: { lines: { show: true } }, yaxis: { lines: { show: false } },
        padding: { top: -20, bottom: -12, left: 0, right: 16 }
      },
      colors: [primary],
      dataLabels: { enabled: false },
      series: [{ name: 'Revenue', data: data.revenue_category_values }],
      xaxis: {
        categories: data.revenue_categories,
        axisBorder: { show: false }, axisTicks: { show: false },
        labels: {
          style: { colors: labelColor, fontFamily, fontSize: '11px' },
          formatter: v => (v >= 1000 ? Math.round(v / 1000) + 'k' : v)
        }
      },
      yaxis: { labels: { style: { colors: labelColor, fontFamily, fontSize: '12px' }, maxWidth: 160 } },
      tooltip: { y: { formatter: aed } }
    }).render();
  }

  // Station network map -- Leaflet over OpenStreetMap tiles
  // --------------------------------------------------------------------
  const mapEl = document.querySelector('#stationMap');
  if (mapEl && typeof L !== 'undefined' && data.map_points) {
    const map = L.map(mapEl, { scrollWheelZoom: false }).setView(data.map_centre, data.map_zoom);

    // Basemap: Esri light-gray canvas plus its reference (label) layer.
    //
    // Chosen over OSM's standard tiles because those render place names in the
    // local script -- Arabic across the UAE -- and this dashboard is read in
    // English. Esri's canvas labels are latin. The neutral grey base also keeps
    // the red station markers the loudest thing on the map.
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

    const fleets = data.map_points.map(p => p.fleet);
    const maxFleet = Math.max.apply(null, fleets) || 1;

    const markers = data.map_points.map(p => {
      // Radius tracks fleet size so the busiest hubs read at a glance.
      const radius = 6 + Math.round((p.fleet / maxFleet) * 14);
      const marker = L.circleMarker([p.lat, p.lng], {
        radius: p.fleet ? radius : 5,
        color: primary,
        weight: 2,
        fillColor: primary,
        fillOpacity: p.fleet ? 0.45 : 0.12
      }).addTo(map);

      marker.bindPopup(
        `<div style="min-width:170px">
           <div style="font-weight:600;margin-bottom:2px">${p.name}</div>
           <div style="opacity:.7;margin-bottom:6px">${p.emirate}</div>
           <div><strong>${p.fleet}</strong> vehicles</div>
           <div><strong>${aed(p.revenue)}</strong> / month</div>
         </div>`
      );
      return marker;
    });

    // Fit to the UAE cluster. The single Kuwait station stays on the map but is
    // excluded from the auto-fit, otherwise the whole Gulf is framed and the UAE
    // network shrinks to a few pixels.
    const core = markers.filter((m, i) => data.map_points[i].emirate !== 'Kuwait');
    const fit = core.length ? core : markers;
    map.fitBounds(L.featureGroup(fit).getBounds().pad(0.12));
    // Re-measure once the card has its final width.
    setTimeout(() => map.invalidateSize(), 250);
  }
})();
