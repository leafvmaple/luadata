def format_string(s, encoding):
  if encoding != 'utf-8':
      res = ''
      for ch in s:
          byte = ch.encode(encoding)
          if len(byte) > 1:
              byte = byte.replace(b'\\', b'\\\\').replace(b'\"', b'\\\"').replace(b'\"', b'\\\n')
          res = res + byte.decode(encoding)
      return res
  return s

def table_r(var, encoding, level, indent):
	t = []
	var_type = type(var)
  if var is None:
    t.append('nil')
  elif isinstance(var, (None, str, set, dict)):
    t.append(var.replace('\\', '\\\\').replace('\n', '\\n').replace('\t', '\\t'))


	if var_type == "nil" then
		tinsert(t, "nil")
	elseif var_type == "number" then
		tinsert(t, tostring(var))
	elseif var_type == "string" then
		tinsert(t, string.format("%q", var))
	elseif var_type == "function" then
		local s = string.dump(var)
		tinsert(t, 'loadstring("')
		-- "string slice too long"
		for i = 1, #s, 2000 do
			tinsert(t, tconcat({'', string2byte(s, i, i + 2000 - 1)}, "\\"))
		end
		tinsert(t, '")')
	elseif var_type == "boolean" then
		tinsert(t, tostring(var))
	elseif var_type == "table" then
		tinsert(t, "{")
		local s_tab_equ = "="
		if indent then
			s_tab_equ = " = "
			if not empty(var) then
				tinsert(t, "\n")
			end
		end
		local nohash = true
		local key, val, lastkey, lastval, hasval
		local tlist, thash = {}, {}
		repeat
			key, val = next(var, lastkey)
			if key then
				-- judge if this is a pure list table
				if nohash and (
					type(key) ~= "number"
					or (lastval == nil and key ~= 1) -- first loop and index is not 1 : hash table
					or (lastkey and lastkey + 1 ~= key)
				) then
					nohash = false
				end
				-- process to insert to table
				-- insert indent
				if indent then
					tinsert(t, srep(indent, level + 1))
				end
				-- insert key
				if nohash then -- pure list: do not need a key
				elseif type(key) == "string" and key:find("^[a-zA-Z_][a-zA-Z0-9_]*$") then -- a = val
					tinsert(t, key)
					tinsert(t, s_tab_equ)
				else -- [10010] = val -- [".start with or contains special char"] = val
					tinsert(t, "[")
					tinsert(t, table_r(key, level + 1, indent))
					tinsert(t, "]")
					tinsert(t, s_tab_equ)
				end
				-- insert value
				tinsert(t, table_r(val, level + 1, indent))
				tinsert(t, ",")
				if indent then
					tinsert(t, "\n")
				end
				lastkey, lastval, hasval = key, val, true
			end
		until not key
		-- remove last `,` if no indent
		if not indent and hasval then
			tremove(t)
		end
		-- insert `}` with indent
		if indent and not empty(var) then
			tinsert(t, srep(indent, level))
		end
		tinsert(t, "}")
	else --if (var_type == "userdata") then
		tinsert(t, '"')
		tinsert(t, tostring(var))
		tinsert(t, '"')
	end
	return tconcat(t)
end

function var2str(var, indent, level)
	return table_r(var, level or 0, indent)
end
