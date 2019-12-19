from pynvim import attach

nvim = attach('socket', path='/tmp/nvim')
result = nvim.api.strwidth("some text")
buf = nvim.current.buffer
length = buf.api.line_count()
print(length)
nvim.exec_lua("""
   local a = vim.api
   local function add(a,b)
       return a+b
   end

   local function buffer_ticks()
      local ticks = {}
      for _, buf in ipairs(a.nvim_list_bufs()) do
          ticks[#ticks+1] = a.nvim_buf_get_changedtick(buf)
      end
      return ticks
   end

   _testplugin = {add=add, buffer_ticks=buffer_ticks}
""")
