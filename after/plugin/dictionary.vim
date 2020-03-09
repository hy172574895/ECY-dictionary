
fun! s:HasECY()
  if exists('g:loaded_easycomplete') && g:loaded_easycomplete == v:true
    return v:true
  endif
  return v:false
endf

if !s:HasECY()
  finish
endif

" a plugin name can not contain space or any symbols.
let s:your_plugin_name = 'dictionary'

" must put these outside a function
" s:current_file_dir look like: /home/myplug/plugin_for_ECY
let  s:current_file_dir = expand( '<sfile>:p:h:h:h' )
let  s:current_file_dir = tr(s:current_file_dir, '\', '/')
let s:client_full_path  = s:current_file_dir . '/dictionary/client/dictionary.py'
let s:server_full_path  = s:current_file_dir . '/dictionary/server/dictionary.py'

"{{{
fun! s:MyInstaller() " called by user. Maybe only once.
  " checked. Must return 'status':0, then return python Server.
  return {'status':'0', 'description':"ok", 'name': s:your_plugin_name}
endf

fun! s:MyUnInstaller() " called by user. Maybe only once.
  return {'status': '0', 'name': s:your_plugin_name}
endf
"}}}

if !exists('g:dictionary_csv_file_path')
  let g:dictionary_csv_file_path = expand( '<sfile>:p:h:h:h' ) . '/ecdict.csv'
  let g:dictionary_csv_file_path = tr(g:dictionary_csv_file_path, '\', '/')
endif

let g:dictionary_frequency_of_filtering_words = 
      \get(g:, 'dictionary_frequency_of_filtering_words', 1000)

let g:dictionary_additional_dict_path = 
      \get(g:, 'dictionary_additional_dict_path', ['C:/Users/qwe/Desktop/google-10000-english-master/20k.txt'])


call ECY#install#AddEngineInfo(s:your_plugin_name, s:client_full_path,
      \s:server_full_path, function('s:MyInstaller'), function('s:MyUnInstaller'))
