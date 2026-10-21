# Umbau Test Dashboard (test-dashboard) auf Menüleiste + Neonplan3D-Farben, 2026-10-21.
# python_transform für ha-mcp ha_config_set_dashboard (eingeschränktes Python, kein def/import).
# Neue Ansichten: home, karl, bkw, wetter, autos, sicherheit. Alte Ansichten bleiben als Unterseiten.
BG = '#070b14'
PANEL = '#0d1628'
TEXT = '#e6eefc'
MUTED = '#a9b8d4'
ACC = '#37e0ff'
LINE = 'rgba(120,190,255,0.22)'
OK = '#4dff80'
WARN = '#ffcc40'
ALARM = '#ff4d40'
WARM = '#ffb547'
TH = 'Neonplan3D'
old = {v.get('path', 'uebersicht'): v for v in config['views']}
np_card = old['neonplan3d']['sections'][0]['cards'][0]
np_card['height'] = 720
np_card['grid_options'] = {'columns': 'full', 'rows': 'auto'}
robi = old['robi']
auto_cards = [c for c in old['auto']['sections'][0]['cards'] if c.get('type') == 'custom:vehicle-status-card']
nav = lambda name, path, icon: {'action': 'navigate', 'navigation_path': '/test-dashboard/' + path, 'name': name, 'active': True, 'icon': icon}
config['sidebar'] = {
    'template': "{% set days = ['Montag','Dienstag','Mittwoch','Donnerstag','Freitag','Samstag','Sonntag'] %}<li>{% if now().hour < 5 %}Gute Nacht,{% elif now().hour < 12 %}Guten Morgen,{% elif now().hour < 18 %}Guten Tag,{% else %}Guten Abend,{% endif %} heute ist {{ days[now().weekday()] }}, der {{ now().strftime('%d.%m.%Y') }}</li>\n{% if 'Müll' in states('calendar.hausordnung') %}<li>Heute Müll rausstellen!</li>{% endif %}\n{% if 'Hausordnung' in states('calendar.hausordnung') %}<li>Heute Hausordnung</li>{% endif %}\n{% if is_state('person.carsten_martens', 'home') %}<li>Carsten ist zuhause 🏠</li>{% elif is_state('person.carsten_martens', 'not_home') %}<li>Carsten ist unterwegs 🚗</li>{% else %}<li>Carsten: {{ states('person.carsten_martens') }}</li>{% endif %}\n{% if is_state('person.elke_martens', 'home') %}<li>Elke ist zuhause 🏠</li>{% elif is_state('person.elke_martens', 'not_home') %}<li>Elke ist unterwegs 🚗</li>{% else %}<li>Elke: {{ states('person.elke_martens') }}</li>{% endif %}\n",
    'width': {'mobile': 0, 'tablet': 20, 'desktop': 20},
    'digitalClock': True,
    'style': ':host {\n  --sidebar-background: ' + PANEL + ';\n  --sidebar-text-color: ' + TEXT + ';\n  --sidebar-icon-color: ' + ACC + ';\n  --sidebar-selected-text-color: ' + ACC + ';\n  --sidebar-selected-icon-color: ' + ACC + ';\n  border-right: 1px solid ' + LINE + ';\n  box-shadow: 0 0 18px rgba(55,224,255,0.15);\n}\n',
    'sidebarMenu': [nav('Home', 'home', 'mdi:home'), nav('Karl', 'karl', 'mdi:robot-vacuum'), nav('Balkonkraftwerk', 'bkw', 'mdi:solar-panel'), nav('Wetter', 'wetter', 'mdi:weather-partly-cloudy'), nav('Autos', 'autos', 'mdi:car-electric'), nav('Sicherheit', 'sicherheit', 'mdi:shield-home'), nav('Räume (alt)', 'uebersicht', 'mdi:floor-plan')],
}
config['kiosk_mode'] = {'hide_sidebar': True, 'hide_header': False, 'mobile_settings': {'hide_header': True}, 'admin_settings': {'hide_sidebar': False, 'hide_header': False}, 'non_admin_settings': {'hide_sidebar': True, 'hide_header': True}}
config['button_card_templates'] = {
    'neon_tile': {'show_icon': True, 'show_name': False, 'show_state': False, 'styles': {
        'card': [{'background': PANEL}, {'border': '1px solid ' + LINE}, {'border-radius': '18px'}, {'padding': '14px'}, {'height': '104px'}, {'box-shadow': '0 0 14px rgba(55,224,255,0.12)'}],
        'grid': [{'grid-template-areas': '"i title" "i text"'}, {'grid-template-columns': '42px 1fr'}, {'grid-template-rows': 'min-content 1fr'}, {'column-gap': '10px'}],
        'icon': [{'width': '26px'}, {'color': ACC}, {'align-self': 'start'}, {'margin-top': '2px'}],
        'custom_fields': {'title': [{'font-size': '12px'}, {'color': MUTED}, {'align-self': 'end'}, {'justify-self': 'start'}, {'text-transform': 'uppercase'}, {'letter-spacing': '0.08em'}],
                          'text': [{'font-size': '19px'}, {'color': TEXT}, {'align-self': 'start'}, {'justify-self': 'start'}, {'text-align': 'left'}, {'line-height': '1.3'}]}}},
    'neon_weather': {'show_icon': True, 'show_name': False, 'show_state': False, 'styles': {
        'card': [{'background': 'linear-gradient(135deg, ' + PANEL + ' 0%, #16223a 100%)'}, {'border': '1px solid ' + LINE}, {'border-radius': '22px'}, {'padding': '20px'}, {'height': '220px'}, {'box-shadow': '0 0 22px rgba(55,224,255,0.18)'}],
        'grid': [{'grid-template-areas': '"i trend" "i temp" "i details"'}, {'grid-template-columns': '110px 1fr'}, {'grid-template-rows': 'min-content 1fr min-content'}, {'column-gap': '18px'}],
        'icon': [{'width': '72px'}, {'color': ACC}, {'justify-self': 'start'}, {'align-self': 'start'}, {'margin-top': '8px'}, {'filter': 'drop-shadow(0 0 8px rgba(55,224,255,0.6))'}],
        'custom_fields': {'trend': [{'justify-self': 'end'}, {'text-align': 'right'}, {'font-size': '18px'}, {'color': MUTED}],
                          'temp': [{'justify-self': 'end'}, {'align-self': 'center'}, {'font-size': '64px'}, {'line-height': '1'}, {'font-weight': '300'}, {'color': TEXT}, {'text-shadow': '0 0 12px rgba(55,224,255,0.45)'}],
                          'details': [{'justify-self': 'end'}, {'text-align': 'right'}, {'font-size': '15px'}, {'line-height': '1.45'}, {'color': MUTED}]}}},
}
neon_style = {'style': 'ha-card {\n  background: ' + PANEL + ';\n  border: 1px solid ' + LINE + ';\n  border-radius: 18px;\n  box-shadow: 0 0 14px rgba(55,224,255,0.12);\n  --primary-text-color: ' + TEXT + ';\n  --secondary-text-color: ' + MUTED + ';\n  --state-icon-color: ' + ACC + ';\n  --primary-color: ' + ACC + ';\n}\n'}
val = lambda e, unit: "[[[ const s = states['" + e + "']; return (s && !['unavailable','unknown'].includes(s.state)) ? s.state + '" + unit + "' : '-'; ]]]"
onoff = lambda on_c, off_c: "[[[ return entity.state === 'on' ? '" + on_c + "' : '" + off_c + "'; ]]]"
tile = lambda e, icon, title, text, cols=8, color=None, tap=None: {'type': 'custom:button-card', 'template': 'neon_tile', 'entity': e, 'icon': icon, 'custom_fields': {'title': title, 'text': text}, 'styles': {'icon': [{'color': color}]} if color else {}, 'tap_action': tap or {'action': 'more-info'}, 'grid_options': {'columns': cols, 'rows': 'auto'}}
head = lambda txt, icon: {'type': 'heading', 'heading': txt, 'icon': icon, 'heading_style': 'title'}
mg = lambda ents, name, cols=24, hours=24, neon_style=neon_style: {'type': 'custom:mini-graph-card', 'name': name, 'entities': ents, 'hours_to_show': hours, 'points_per_hour': 4, 'line_width': 3, 'height': 140, 'animate': True, 'show': {'fill': 'fade', 'legend': True, 'icon': False}, 'card_mod': neon_style, 'grid_options': {'columns': cols, 'rows': 'auto'}}
sec = lambda cards: {'type': 'grid', 'column_span': 4, 'cards': cards}
view = lambda title, path, icon, sections, badges=[], TH=TH: {'type': 'sections', 'title': title, 'path': path, 'icon': icon, 'theme': TH, 'max_columns': 4, 'dense_section_placement': True, 'badges': badges, 'sections': sections}
person = lambda e, name, icon: {'type': 'custom:mushroom-template-badge', 'entity': e, 'icon': icon, 'content': name, 'color': "{{ 'cyan' if is_state(entity, 'home') else 'grey' }}"}
v_home = view('Home', 'home', 'mdi:home', [sec([np_card])], [person('person.carsten_martens', 'Carsten', 'mdi:face-man-outline'), person('person.elke_martens', 'Elke', 'mdi:face-woman-outline')])
karl_cards = [c for c in robi['sections'][0]['cards'] if c.get('type') != 'vertical-stack']
v_karl = view('Karl', 'karl', 'mdi:robot-vacuum', [sec([head('🧹 Karl (Mova Z60)', '')] + karl_cards)])
akku_c = "[[[ const l = parseFloat(states['sensor.solakon_one_batterie_ladestand']?.state); return isNaN(l) ? '" + MUTED + "' : (l > 50 ? '" + OK + "' : (l > 20 ? '" + WARN + "' : '" + ALARM + "')); ]]]"
v_bkw = view('Balkonkraftwerk', 'bkw', 'mdi:solar-panel', [
    sec([head('☀️ Jetzt', ''),
         tile('sensor.solakon_one_pv_leistung', 'mdi:solar-power-variant', 'PV-Leistung', val('sensor.solakon_one_pv_leistung', ' W'), 8, WARM),
         tile('sensor.solakon_one_leistung', 'mdi:transmission-tower-export', 'Ausgang', val('sensor.solakon_one_leistung', ' W')),
         tile('sensor.solakon_one_batterie_ladestand', 'mdi:battery-high', 'Akku', val('sensor.solakon_one_batterie_ladestand', ' %'), 8, akku_c),
         tile('sensor.energy_production_today', 'mdi:chart-bell-curve', 'Prognose heute', val('sensor.energy_production_today', ' kWh')),
         tile('sensor.energy_production_today_remaining', 'mdi:timer-sand', 'Rest heute', val('sensor.energy_production_today_remaining', ' kWh')),
         tile('sensor.energy_production_tomorrow', 'mdi:weather-sunny', 'Prognose morgen', val('sensor.energy_production_tomorrow', ' kWh'))]),
    sec([head('📈 Verlauf', ''),
         mg([{'entity': 'sensor.solakon_one_pv_leistung', 'name': 'PV', 'color': WARM}, {'entity': 'sensor.solakon_one_leistung', 'name': 'Ausgang', 'color': ACC}], 'Leistung 24 h'),
         mg([{'entity': 'sensor.solakon_one_batterie_ladestand', 'name': 'Akku', 'color': OK}], 'Akku 24 h'),
         mg([{'entity': 'sensor.solakon_one_string_1_leistung', 'name': 'String 1', 'color': ACC}, {'entity': 'sensor.solakon_one_string_2_leistung', 'name': 'String 2', 'color': '#ff5fd2'}, {'entity': 'sensor.solakon_one_string_3_leistung', 'name': 'String 3', 'color': WARM}, {'entity': 'sensor.solakon_one_string_4_leistung', 'name': 'String 4', 'color': OK}], 'Strings 24 h', 48)]),
    sec([head('⚙️ Nulleinspeisung und Speicher', ''),
         {'type': 'entities', 'card_mod': neon_style, 'grid_options': {'columns': 24, 'rows': 'auto'}, 'entities': ['input_boolean.solarkon_einspeisung', 'input_boolean.solakon_ac_laden_aktiv', 'input_number.solakon_einspeisewert', 'input_number.solakon_pv_mindeswert', 'input_number.solakon_mindesteinspeisung', 'input_number.solakon_akku_uberlaufschwelle']},
         {'type': 'entities', 'card_mod': neon_style, 'grid_options': {'columns': 24, 'rows': 'auto'}, 'entities': ['input_number.maximalwert_speicher', 'input_number.mindestwert_speicher', 'input_number.maximale_einspeisung', 'sensor.solakon_one_wechselrichter_temperatur', 'sensor.solakon_one_batterie_max_temperatur', 'sensor.solakon_one_batterie_min_temperatur', 'sensor.solakon_one_batterie_gesundheitszustand']},
         {'type': 'entities', 'title': 'Zählerstände', 'card_mod': neon_style, 'grid_options': {'columns': 48, 'rows': 'auto'}, 'entities': ['sensor.solakon_one_pv_energie', 'sensor.solakon_one_netz_exportenergie', 'sensor.solakon_one_netz_importenergie']}]),
])
warn = lambda e, icon, title, txt, tap, tile=tile, onoff=onoff, ALARM=ALARM, OK=OK: tile(e, icon, title, "[[[ return states['" + txt + "']?.state || '-'; ]]]", 16, onoff(ALARM, OK), {'action': 'perform-action', 'perform_action': tap})
v_wetter = view('Wetter', 'wetter', 'mdi:weather-partly-cloudy', [
    sec([{'type': 'custom:button-card', 'template': 'neon_weather', 'entity': 'sensor.ws2350_v2_38_outdoor_temperature', 'icon': 'mdi:weather-partly-cloudy', 'grid_options': {'columns': 24, 'rows': 'auto'},
          'custom_fields': {'trend': "[[[ return states['sensor.openweathermap_wetter']?.state || '-'; ]]]",
                            'temp': "[[[ return `${states['sensor.ws2350_v2_38_outdoor_temperature']?.state || '-'}°C`; ]]]",
                            'details': "[[[ const h = states['sensor.ws2350_v2_38_humidity']?.state || '-'; const w = states['sensor.windgeschwindigkeit_10min_durchschnitt']?.state || '-'; const uv = states['sensor.ws2350_v2_38_uv_index']?.state || '-'; return `${h}% Luftfeuchte<br>${w} km/h Wind<br>UV ${uv}`; ]]]"}},
         {'type': 'weather-forecast', 'entity': 'weather.itzgrund_herreth', 'show_current': True, 'show_forecast': True, 'forecast_type': 'daily', 'round_temperature': True, 'card_mod': neon_style, 'grid_options': {'columns': 24, 'rows': 'auto'}},
         {'type': 'weather-forecast', 'entity': 'weather.itzgrund_herreth', 'show_current': False, 'show_forecast': True, 'forecast_type': 'hourly', 'card_mod': neon_style, 'grid_options': {'columns': 48, 'rows': 'auto'}}]),
    sec([head('⚠️ Warnungen', ''),
         warn('binary_sensor.statusseite_nina_warnung_aktiv', 'mdi:alert', 'NINA', 'sensor.statusseite_nina_warnungen_text', 'script.dashboard_alarm_detail_show_nina'),
         warn('binary_sensor.statusseite_wetterwarnung_aktiv', 'mdi:weather-lightning-rainy', 'Wetter', 'sensor.statusseite_wetterwarnung_text', 'script.dashboard_alarm_detail_show_wetter'),
         warn('binary_sensor.statusseite_pollenwarnung_aktiv', 'mdi:flower-pollen', 'Pollenflug', 'sensor.statusseite_pollenwarnung_text', 'script.dashboard_alarm_detail_show_pollen')]),
    sec([head('🌬️ Wind und Radar', ''),
         {'type': 'custom:windrose-card', 'title': 'Windrichtung', 'data_period': {'period_back': '-12h'}, 'refresh_interval': 300, 'windspeed_bar_location': 'right', 'wind_direction_entity': {'entity': 'sensor.windrichtung_10min_durchschnitt', 'use_statistics': False}, 'windspeed_entities': [{'entity': 'sensor.windgeschwindigkeit_10min_durchschnitt', 'name': 'Wind', 'speed_unit': 'auto', 'output_speed_unit': 'kmh', 'speed_range_beaufort': True}], 'direction_labels': {'cardinal_direction_letters': 'NOSW'}, 'current_direction': {'show_arrow': True}, 'card_mod': neon_style, 'grid_options': {'columns': 24, 'rows': 'auto'}},
         {'type': 'iframe', 'url': 'https://embed.windy.com/embed.html?type=map&location=coordinates&metricRain=default&metricTemp=default&metricWind=default&zoom=8&overlay=rain&product=ecmwf&level=surface&lat=50.195&lon=10.970&detailLat=50.195&detailLon=10.970&marker=true&message=true', 'aspect_ratio': '100%', 'card_mod': neon_style, 'grid_options': {'columns': 24, 'rows': 8}}]),
])
for c in auto_cards:
    c['range_info'][0]['progress_color'] = ACC
    c['card_mod'] = neon_style
    c['grid_options'] = {'columns': 24, 'rows': 'auto'}
auto_cards[0]['mini_map']['device_tracker'] = 'device_tracker.mg_mgs5_ev_gps_location'
home_txt = lambda zuhause, soc: "[[[ const z = states['" + zuhause + "']?.state === 'on' ? 'Zuhause' : 'Unterwegs'; const s = states['" + soc + "']?.state; return `${z} · ${s && !isNaN(parseFloat(s)) ? Math.round(parseFloat(s)) + ' %' : '-'}`; ]]]"
v_autos = view('Autos', 'autos', 'mdi:car-electric', [
    sec([head('🚗 Status', ''),
         tile('binary_sensor.auto_mg_zuhause', 'mdi:car-electric', 'MG MGS5', home_txt('binary_sensor.auto_mg_zuhause', 'sensor.mg_mgs5_ev_state_of_charge'), 16, onoff(OK, MUTED)),
         tile('binary_sensor.auto_capri_zuhause', 'mdi:car-electric-outline', 'Ford Capri', home_txt('binary_sensor.auto_capri_zuhause', 'sensor.fordpass_wf0spbef1tsd01110_soc'), 16, onoff(OK, MUTED)),
         tile('binary_sensor.auto_capri_eingesteckt', 'mdi:ev-plug-type2', 'Capri Ladekabel', "[[[ return entity.state === 'on' ? 'Eingesteckt' : 'Nicht eingesteckt'; ]]]", 16, onoff(ACC, MUTED))]),
    sec([head('🔋 Fahrzeuge', '')] + auto_cards),
    sec([head('📒 Fahrtenbuch Capri', ''),
         {'type': 'entities', 'title': 'Letzte Fahrt', 'card_mod': neon_style, 'grid_options': {'columns': 24, 'rows': 'auto'}, 'entities': [{'entity': 'sensor.aussen_fartenbuch_last_start_address', 'name': 'Start'}, {'entity': 'sensor.aussen_fartenbuch_last_end_address', 'name': 'Ziel'}, {'entity': 'sensor.aussen_fartenbuch_last_distance', 'name': 'Strecke'}, {'entity': 'sensor.aussen_fartenbuch_last_driving_time', 'name': 'Fahrzeit'}, {'entity': 'sensor.aussen_fartenbuch_last_efficiency', 'name': 'Verbrauch je 100 km'}]},
         {'type': 'entities', 'title': 'Gesamt', 'card_mod': neon_style, 'grid_options': {'columns': 24, 'rows': 'auto'}, 'entities': [{'entity': 'binary_sensor.aussen_fartenbuch_trip_active', 'name': 'Aktive Fahrt'}, {'entity': 'sensor.aussen_fartenbuch_trip_count', 'name': 'Fahrten'}, {'entity': 'sensor.aussen_fartenbuch_total_distance', 'name': 'Gesamtkilometer'}, {'entity': 'sensor.aussen_fartenbuch_average_consumption', 'name': 'Ø Verbrauch'}, {'entity': 'sensor.aussen_fartenbuch_charge_count', 'name': 'Ladevorgänge'}]}]),
])
v_sicher = view('Sicherheit', 'sicherheit', 'mdi:shield-home', [
    sec([head('🛡️ Status', ''),
         tile('binary_sensor.haus_fenster_offen', 'mdi:window-closed-variant', 'Fenster', "[[[ return states['sensor.fenster_status_text']?.state || '-'; ]]]", 12, onoff(ALARM, OK)),
         tile('binary_sensor.haus_turen_offen', 'mdi:door-closed', 'Türen', "[[[ return states['sensor.turen_status_text']?.state || '-'; ]]]", 12, onoff(ALARM, OK)),
         tile('binary_sensor.homematic_ip_turkontakt_keller', 'mdi:door', 'Kellertür', "[[[ return entity.state === 'on' ? 'Offen' : 'Geschlossen'; ]]]", 12, onoff(ALARM, OK)),
         tile('binary_sensor.statusseite_hausalarm_aktiv', 'mdi:home-alert-outline', 'Hausalarm', "[[[ return states['sensor.statusseite_hausalarm_text']?.state || '-'; ]]]", 12, onoff(ALARM, OK))]),
    sec([head('🚨 Alarmo', ''),
         {'type': 'custom:alarmo-card', 'entity': 'alarm_control_panel.home', 'name': 'Haus', 'card_mod': neon_style, 'grid_options': {'columns': 24, 'rows': 'auto'}},
         {'type': 'custom:alarmo-card', 'entity': 'alarm_control_panel.keller', 'name': 'Keller', 'card_mod': neon_style, 'grid_options': {'columns': 24, 'rows': 'auto'}}]),
    sec([head('🎥 Kameras', ''),
         {'type': 'picture-entity', 'entity': 'camera.terrasse', 'name': 'Terrasse', 'camera_view': 'auto', 'card_mod': neon_style, 'grid_options': {'columns': 24, 'rows': 'auto'}},
         {'type': 'picture-entity', 'entity': 'camera.tb361fu', 'name': 'Flur (Tablet)', 'camera_view': 'auto', 'card_mod': neon_style, 'grid_options': {'columns': 24, 'rows': 'auto'}}]),
])
keep = []
for p, v in old.items():
    if p in ('neonplan3d', 'robi', 'bkw', 'auto', 'cameras'):
        continue
    v['path'] = p
    v['subview'] = True
    v['theme'] = TH
    keep.append(v)
remap = {'/test-dashboard/robi': '/test-dashboard/karl', '/test-dashboard/cameras': '/test-dashboard/sicherheit', '/test-dashboard/auto': '/test-dashboard/autos', '/test-dashboard/wohnbereich': '/test-dashboard/wohnzimmer', '/test-dashboard/kueche': '/test-dashboard/kuche', '/test-dashboard/buero': '/test-dashboard/buro', '/test-dashboard': '/test-dashboard/home'}
stack = list(keep)
for _ in range(20000):
    if not stack:
        break
    x = stack.pop()
    if isinstance(x, dict):
        if x.get('navigation_path') in remap:
            x['navigation_path'] = remap[x['navigation_path']]
        stack.extend([y for y in x.values() if isinstance(y, (dict, list))])
    elif isinstance(x, list):
        stack.extend([y for y in x if isinstance(y, (dict, list))])
config['views'] = [v_home, v_karl, v_bkw, v_wetter, v_autos, v_sicher] + keep
