
//rAthena viewpointmap (thank you Winterfox :D)

//Add anywhere inside the BUILDIN_FUNC's
int viewpointmap_sub(struct block_list *bl, va_list ap) {
	struct map_session_data *sd;
	int npc_id, type, x, y, id, color;
	npc_id = va_arg(ap, int);
	type = va_arg(ap, int);
	x = va_arg(ap, int);
	y = va_arg(ap, int);
	id = va_arg(ap, int);
	color = va_arg(ap, int);
	sd = (struct map_session_data *)bl;
	clif_viewpoint(sd, npc_id, type, x, y, id, color);

	return 0;

}

BUILDIN_FUNC(viewpointmap) {
	int type, x, y, id, color, m;
	const char *map_name;
	map_name = script_getstr(st, 2);

	if ((m = map_mapname2mapid(map_name)) < 0)
		return true; // Invalid Map

	type = script_getnum(st, 3);
	x = script_getnum(st, 4);
	y = script_getnum(st, 5);
	id = script_getnum(st, 6);
	color = script_getnum(st, 7);
	map_foreachinmap(viewpointmap_sub, m, BL_PC, st->oid, type, x, y, id, color);
	return true;
}


// Add this to the list of script commands defined, look through the code, should be self explanitory.
	BUILDIN_DEF(viewpointmap,"siiiii"),