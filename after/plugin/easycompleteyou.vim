
fun! s:HasECY()
  if exists('g:loaded_easycomplete') && g:loaded_easycomplete == v:true
    return v:true
  endif
  return v:false
endf

fun! s:Regist(installer, uninstaller, client_lib, client_path, engine_name) " called after vim started.
  call ECY#install#RegisterClient(a:engine_name, a:client_lib, a:client_path)
  call ECY#install#RegisterInstallFunction(a:engine_name, function(a:installer))
  call ECY#install#RegisterUnInstallFunction(a:engine_name, function(a:uninstaller))
endf

" ==============================================================================
" you can just copy the above. What you need to modify is the following.
" ==============================================================================

" a plugin name can not contain space or any symbols.
let s:your_plugin_name = 'dictionary'

" must put these outside a function
" s:current_file_dir look like: /home/myplug/plugin_for_ECY
let  s:current_file_dir = expand( '<sfile>:p:h:h:h' )
let  s:current_file_dir = tr(s:current_file_dir, '\', '/')

fun! s:MyInstaller() " called by user. Maybe only once.
  " 1
  " you should check your plugin dependencies here.
  if !exists('g:my_plugin_dictionary_file_path')
    return {'status':'-1',
          \'description':"You must set a dictionary file. Failed to enable dictionary that is a plugin of ECY."}
  endif

  " 2
  " checked. Must return 'status':0, then return python Server.
  return {'status':'0',
        \'description':"ok", 'lib':
        \'dictionary.server.dictionary', 
        \'name': s:your_plugin_name, 
        \'path': s:current_file_dir
        \}
endf

fun! s:MyUnInstaller() " called by user. Maybe only once.
  return {'status': '0', 'name': s:your_plugin_name}
endf

if !s:HasECY()
  finish
endif

if !exists('g:my_plugin_dictionary_file_path')
  let g:my_plugin_dictionary_file_path = expand( '<sfile>:p:h:h:h' ) . '/ecdict.csv'
  let g:my_plugin_dictionary_file_path = tr(g:my_plugin_dictionary_file_path, '\', '/')
endif

" (installer, uninstaller, client_lib, client_path, engine_name)
call s:Regist(
      \'s:MyInstaller',
      \'s:MyUnInstaller',
      \'dictionary.client.dictionary',
      \s:current_file_dir,
      \s:your_plugin_name)
