from pynvim import attach
import time
nvim = attach('socket', path='/tmp/nvim')

# Get current buffer
# buf = nvim.current.buffer

# # Replace line 0
# buf[0] = 'replaced done'
# 
# # Set global var 
# nvim.vars['global_var'] = [1, 2, 3]
# nvim.eval('g:global_var')
# 
# # Get length
# length = nvim.request("nvim_buf_line_count", buf)
# 
# # Highlight and clear
# ## Create a namespace to manage highlights
# nid = nvim.request("nvim_create_namespace", "something")
# 
# # params are curr_buffer, namespace_id, hl_group, row, column start, column end
# ## Highlight group can be found from :highlight
# ev = nvim.request("nvim_buf_add_highlight", 0, nid, "PMenu", 0, 0, -1)
# time.sleep(2)
# 
# # Clear namespace
# ev = nvim.request("nvim_buf_clear_namespace", 0, nid, 0, -1)
# 
# # Find and highlight 
# ## Put some text
# ### Third argument is an insertion type mode, 4t is after cursour, fifth is position of cursor after this api
# #ev = nvim.request("nvim_put", ["trying this api"], "l", 1, 1)
# 
# # Add text the normal way
# # buf.append("Some new text")
# # buf.append("Some old text")
# 
# 
# ## Trying global out
# g = nvim.eval("search('done')")
# print(g)
# g = nvim.eval("search('text')")
# print(g)
# 
# 
# # Callback test 
# 
# cid = nvim.channel_id
# print(cid)
# 
# def setup_cb():
#     cmd = 'let g:result = rpcrequest(%d, "func")' % cid
#     nvim.command(cmd)
#     # assert nvim.vars['result'] == [4, 5, 6]
#     print(nvim.vars['result'])
#     nvim.stop_loop()
# 
# def request_cb(name, args):
#     print(name)
#     print(args)
# 
# # Subscribe to buffer
# nvim.run_loop(request_cb, None, setup_cb)
# 
# 
# 
# # # Receiving events
# # def test_receiving_events(nvim):
# #     print("Receiving events")
# #     print(nvim.channel_id)
# #     nvim.command('call rpcnotify(%d, "test-event", 1, 2, 3)' % nvim.channel_id)
# #     event = nvim.next_message()
# #     print(event)
# #     nvim.command('au FileType python call rpcnotify(%d, "py!", bufnr("$"))' % nvim.channel_id)
# #     nvim.command('set filetype=python')
# #     event = nvim.next_message()
# #     print(event)
# # 
# # test_receiving_events(nvim)
# 
# 
# 
# 
# # Testing broadcast
# nvim.subscribe('event2')
# nvim.command('call rpcnotify(0, "event1", 1, 2, 3)')
# # Unicast
# nvim.command('call rpcnotify(%d, "event2", 4, 5, 6)' % nvim.channel_id)
# nvim.command('call rpcnotify(0, "event2", 7, 8, 9)')
# event = nvim.next_message()
# print(event)
# event = nvim.next_message()
# print(event)
# nvim.unsubscribe('event2')
# nvim.subscribe('event1')
# nvim.command('call rpcnotify(0, "event2", 10, 11, 12)')
# nvim.command('call rpcnotify(0, "event1", 13, 14, 15)')
# msg = nvim.next_message()
# print(msg)



def search_pattern(pattern):
    idxs = []
    hdls = []
    lns = []
    hid = nvim.request("nvim_create_namespace", pattern)
    while True:
        l = nvim.eval("searchpos('%s', 'w')" % pattern)
        if l in idxs:
            break
        idxs.append(l)
        hdls.append(nvim.request("nvim_buf_add_highlight", 0, hid, "PMenu", l[0], 0, -1))
        lns.append(nvim.eval("getline(%d)" % l[0]))   

    return lns, hid

lst, hid = search_pattern("ok")
nvim.request("nvim_buf_clear_namespace", 0, hid, 0, -1)
print(lst)
