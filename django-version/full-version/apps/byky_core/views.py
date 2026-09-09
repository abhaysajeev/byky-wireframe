"""Shared view base for BYKY wireframe screens.

Every BYKY screen goes through TemplateLayout.init so the Vuexy layout context
(menu, navbar, theme, container classes) is present. Screens carry their FSD
identity in the context so placeholders and page headers can render it without
each view repeating itself.
"""

from django.views.generic import TemplateView

from web_project import TemplateLayout
from web_project.template_helpers.theme import TemplateHelper

from . import drawers as core_drawers


class BykyScreenView(TemplateView):
    # Set per-route in each module's urls.py.
    screen_no = ""
    screen_title = ""
    module_label = ""
    legacy_page = ""
    tier = "A"
    phase = 0
    purpose = ""
    layout = ""

    # {template_var: drawer spec} for the module, set on each module's base
    # view (e.g. CmsScreenView.drawer_specs = drawers.SPECS).
    drawer_specs = {}

    TIER_LABEL = {
        "A": "List + drawer form",
        "B": "List + full-page form",
        "C": "Read-only monitor / report",
        "D": "Permission matrix",
    }

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context.update(
            {
                "screen_no": self.screen_no,
                "screen_title": self.screen_title,
                "module_label": self.module_label,
                "legacy_page": self.legacy_page,
                "tier": self.tier,
                "tier_label": self.TIER_LABEL.get(self.tier, ""),
                "phase": self.phase,
                "purpose": self.purpose,
                "layout": self.layout,
            }
        )
        TemplateHelper.map_context(context)
        return context

    def render_to_response(self, context, **kwargs):
        """Resolve the module's drawer specs against the finished context.

        Done here rather than in get_context_data because a select's options
        come from lists a *subclass* adds after calling super() -- by then the
        base has already returned and cannot see them. At render time the
        context is complete.
        """
        if self.drawer_specs:
            context.update(core_drawers.resolve_all(self.drawer_specs, context))
        return super().render_to_response(context, **kwargs)


class BykyDashboardView(TemplateView):
    """BYKY landing dashboard.

    Mixes the commercial picture (revenue, rentals, average ticket) with the
    operational one (fleet, stations, utilisation) and a live network map.

    Fleet, station and workforce figures come from the client's own data via
    apps/byky_core/seed.py. Revenue figures are indicative and generated in
    apps/byky_core/sales.py -- the client's files carry no transactions. The
    page labels them as such.
    """

    template_name = "byky_dashboard.html"

    def get_context_data(self, **kwargs):
        from apps.byky_core import geo, sales, seed

        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context.update(seed.dashboard())

        head = sales.headline()
        stations = sales.by_station()
        daily = sales.daily_series()
        monthly = sales.monthly_series()

        # Marker payload for the Leaflet/OpenStreetMap network map.
        points = []
        for st in stations:
            c = geo.coords_for(st["name"])
            if not c:
                continue
            points.append(
                {
                    "name": st["name"],
                    "emirate": st["emirate"],
                    "fleet": st["fleet"],
                    "revenue": st["revenue"],
                    # indicative, like revenue -- see sales.on_rent_share
                    "on_rent": st["on_rent"],
                    "lat": c[0],
                    "lng": c[1],
                }
            )

        context.update(
            {
                "sales": head,
                "top_stations_revenue": stations[:6],
                "revenue_by_emirate": sales.by_emirate(),
                "revenue_by_category": sales.by_category(),
                "invoices": sales.recent_invoices(),
                "map_points": points,
                "map_centre": list(geo.UAE_CENTRE),
                "map_zoom": geo.UAE_ZOOM,
            }
        )

        # Series handed to ApexCharts / Leaflet through json_script.
        context["chart_data"] = dict(
            context.get("chart_data", {}),
            daily_labels=[d["label"] for d in daily],
            daily_revenue=[d["revenue"] for d in daily],
            monthly_labels=[m["label"] for m in monthly],
            monthly_revenue=[m["revenue"] for m in monthly],
            revenue_emirates=[e for e, _ in sales.by_emirate()],
            revenue_emirate_values=[v for _, v in sales.by_emirate()],
            revenue_categories=[c for c, _ in sales.by_category()],
            revenue_category_values=[v for _, v in sales.by_category()],
            map_points=points,
            map_centre=list(geo.UAE_CENTRE),
            map_zoom=geo.UAE_ZOOM,
        )
        TemplateHelper.map_context(context)
        return context


class GenericScreenView(BykyScreenView):
    """Renders a screen from its declarative spec (apps/byky_core/screens.py).

    Set `spec` per route. When `get_rows` yields nothing the screen still draws its
    column headers, with the awaiting-data state inside the table body.
    """

    template_name = "byky/generic_screen.html"
    spec = None
    rows = ()
    awaiting = ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.reference_lists())

        spec = dict(self.spec or {})
        # Resolve `source` names into concrete option lists for filters and fields.
        spec["filters"] = [self._resolve(f, context) for f in spec.get("filters", [])]
        spec["sections"] = [
            {"title": s["title"], "fields": [self._resolve(f, context) for f in s["fields"]]}
            for s in spec.get("sections", [])
        ]
        context.update(
            {
                "spec": spec,
                "rows": self.get_rows(),
                "awaiting": self.awaiting,
                "drawer_href": "#" + spec.get("drawer_id", "offcanvasAdd"),
            }
        )
        return context

    def _resolve(self, item, context):
        item = dict(item)
        src = item.get("source")
        if src:
            values = context.get(src, [])
            item["resolved"] = [
                (v.get("name") or v.get("title") or v.get("emp_no", "")) if isinstance(v, dict) else v
                for v in values
            ]
        else:
            item["resolved"] = item.get("options", [])
        return item

    def reference_lists(self):
        """Overridden per module to supply dropdown sources."""
        return {}

    def get_rows(self):
        return self.rows
