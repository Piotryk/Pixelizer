import PySimpleGUI as sg

img_resize_target = 768
img_resize_start = 512


def make_window(mode):

    sg.theme('DarkAmber')
    #background_color = '#dddddd'
    background_color = '#2c2825'

    slider_res_range = (4, 256)
    slider_col_range = (1, 64)
    slider_size = (15, 16)

    if mode == '4k':
        size_control_column = (460, 750)
        size_main_image = (1024, 1024)
        size_window = (1270, 550)
        font = 'Helvetica 12'
    elif mode == 'riddles':
        size_control_column = (560, 750)
        size_main_image = (img_resize_target, img_resize_target)
        size_window = (600 + img_resize_target, img_resize_target + 50)
        font = 'Helvetica 12'
        slider_res_range = (4, 512)
        slider_col_range = (1, 128)
        slider_size = (30, 16)
    else:   # Standard Full HD. Everything / 2
        """ WIP """
        size_control_column = (500, 650)
        size_main_image = (512, 512)
        size_window = (1270, 620)
        font = 'Helvetica 6'

    control_col = sg.Column(layout=[
        [sg.Text('', key='FILLER_1', size=(1, 1), expand_y=False)],
        [sg.Text('Original image resolution: ', ), sg.Text('', key='INFO_ORIGINAL_RES')],
        [sg.Frame('Settings', expand_x=True, layout=[
            #[sg.Button('Select Image', key='SELECT')],
            [sg.FileBrowse("Select Image", key='SELECT', enable_events=True)],
            [sg.Text('', key='FILLER_3', size=(1, 1), expand_y=False)],
            [sg.Checkbox('Keep Ratio', key='BUTTON_RATIO', default=True, enable_events=True)],
            [sg.Text('\nx resolution: ', size=(10, 2)),
             sg.pin(sg.Input(size=(5, 1), key='INPUT_X', enable_events=True, expand_x=False, visible=True), vertical_alignment='b', ),
             sg.Button('', key='ENTER_RES', bind_return_key=True, visible=False),
             sg.Slider(size=slider_size, key='SLIDER_X', range=slider_res_range, default_value=slider_res_range[1], orientation='h', enable_events=True),
             ],
            [sg.Text('\ny resolution: ', size=(10, 2)),
             sg.pin(sg.Input(size=(5, 1), key='INPUT_Y', enable_events=True, expand_x=False, visible=True), vertical_alignment='b', ),
             # sg.Button('', key='ENTER_RES_Y', bind_return_key=True, visible=False),
             sg.Slider(size=slider_size, key='SLIDER_Y', range=slider_res_range, default_value=slider_res_range[1], orientation='h', enable_events=True),
             ],
            [sg.Button('Resolution: + 1', key='BUTTON_RESOLUTION_INC_1')],
            [sg.Button('Resolution: + 5', key='BUTTON_RESOLUTION_INC_5')],
            [sg.Text('', key='FILLER_4', size=(2, 1), expand_y=False)],
            [sg.Text('\nNumber of colors: ', expand_x=True),
             sg.Slider(size=slider_size, key='SLIDER_COLOR', range=slider_col_range, default_value=slider_col_range[1], orientation='h', enable_events=True),
             ],
            [sg.Button('Reset Image', key='RESET'), sg.Text('', key='FILLER_5', size=(34, 1), expand_y=True), sg.Button('⭯', key='ROTATE_LEFT'), sg.Button('⭮', key='ROTATE_RIGHT')]
        ])],
        [sg.Text('DEBUG INFO: ', visible=True, key='DEBUG_INFO'),
         sg.Text('Start with selecting image', expand_x=True, justification='left', visible=True, key='DEBUG')],
    ], size=size_control_column, pad=1, vertical_alignment='top', key='CCOL')

    main_image = sg.Image('', key='IMAGE', size=size_main_image, background_color=background_color, enable_events=True, visible=True, )

    layout = [[control_col, main_image]]

    window = sg.Window('Image Resizer', layout, size=size_window, finalize=True, resizable=True, element_justification='center', font=font)
    return window
