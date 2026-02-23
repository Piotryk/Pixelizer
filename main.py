from PIL import Image
import io
import PySimpleGUI as sg
import window

img_size = window.img_resize_target


def debug(main_window, text):
    main_window['DEBUG'].update(text)
    main_window.refresh()


def draw_figure(image_element, img):
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    imgbytes = buf.getvalue()
    image_element.update(data=imgbytes, size=(window.img_resize_target, window.img_resize_target))


def main(mode):
    original_image = current_img = None
    original_size = real_size = None
    flag_resized = False
    flag_recolored = False

    main_window = window.make_window(mode)

    # MAIN LOOP
    while True:
        event, values = main_window.read()
        #print(event, values)
        #relative_mouse_location = (main_window.mouse_location()[0] - main_window.CurrentLocation()[0], main_window.mouse_location()[1] - main_window.CurrentLocation()[1])
        #print(relative_mouse_location)

        if event == sg.WIN_CLOSED:
            main_window.close()
            break

        if event == 'SELECT':
            image_path = values['SELECT']
            original_image = Image.open(image_path)  #.resize(size_main_image)
            original_size = real_size = original_image.size

            current_img = original_image

            if original_size[0] > img_size or original_size[1] > img_size:
                ratio = max(original_size[0], original_size[1]) / img_size
                real_size = (int(original_size[0] / ratio), int(original_size[1] / ratio))
                current_img = original_image.resize((10, 10), resample=Image.Resampling.BILINEAR)

            #draw_figure(main_window['IMAGE'], current_img)
            debug(main_window, f'Showing image {real_size}')
            main_window['INFO_ORIGINAL_RES'].update(f'{original_size[0]} x {original_size[1]}')
            main_window['SLIDER_X'].update(int(4))
            main_window['SLIDER_Y'].update(int(4))
            #event = 'SLIDER_X'
            if original_size[0] < original_size[1]:
                x_res = 4
                y_res = int(4 / original_size[0] * original_size[1])
            else:
                x_res = int(4 / original_size[1] * original_size[0])
                y_res = 4

            current_res = (x_res, y_res)
            main_window['SLIDER_X'].update(int(x_res))
            main_window['SLIDER_Y'].update(int(y_res))
            imgSmall = current_img.resize(current_res, resample=Image.Resampling.BILINEAR)
            img = imgSmall.resize(real_size, Image.Resampling.NEAREST)

            draw_figure(main_window['IMAGE'], img)

        # todo: note
        if original_image is None:
            continue

        if event == 'BUTTON_RESOLUTION_INC_1':
            current_res = (int(values['SLIDER_X']) + 1, int(values['SLIDER_Y']) + 1)

            #main_window['SLIDER_X'].update(int(values['SLIDER_X']) + 1)
            #main_window['SLIDER_Y'].update(int(values['SLIDER_Y']) + 1)

            if values['SLIDER_X'] < values['SLIDER_Y']:
                x_res = values['SLIDER_X'] + 1
                y_res = int(x_res / original_size[0] * original_size[1])
            else:
                y_res = values['SLIDER_Y'] + 1
                x_res = int(y_res / original_size[1] * original_size[0])

            main_window['SLIDER_X'].update(int(x_res))
            main_window['SLIDER_Y'].update(int(y_res))

            img = original_image
            if flag_recolored:
                img = img.convert('P', palette=Image.ADAPTIVE, colors=int(values['SLIDER_COLOR']))

            imgSmall = img.resize(current_res, resample=Image.Resampling.NEAREST)
            img = imgSmall.resize(real_size, Image.Resampling.NEAREST)

            draw_figure(main_window['IMAGE'], img)
            debug(main_window, f'resized image to {current_res}')
            flag_resized = True

        if event == 'BUTTON_RESOLUTION_INC_5':
            inc = 5
            current_res = (int(values['SLIDER_X']) + inc, int(values['SLIDER_Y']) + inc)
            #main_window['SLIDER_X'].update(int(values['SLIDER_X']) + inc)
            #main_window['SLIDER_Y'].update(int(values['SLIDER_Y']) + inc)

            if values['SLIDER_X'] < values['SLIDER_Y']:
                x_res = values['SLIDER_X'] + 5
                y_res = int(x_res / original_size[0] * original_size[1])
            else:
                y_res = values['SLIDER_Y'] + 5
                x_res = int(y_res / original_size[1] * original_size[0])

            main_window['SLIDER_X'].update(int(x_res))
            main_window['SLIDER_Y'].update(int(y_res))

            img = original_image
            if flag_recolored:
                img = img.convert('P', palette=Image.ADAPTIVE, colors=int(values['SLIDER_COLOR']))

            imgSmall = img.resize(current_res, resample=Image.Resampling.NEAREST)
            img = imgSmall.resize(real_size, Image.Resampling.NEAREST)

            draw_figure(main_window['IMAGE'], img)
            debug(main_window, f'resized image to {current_res}')
            flag_resized = True

        if event == 'SLIDER_X':
            if values['BUTTON_RATIO']:
                y_res = values['SLIDER_X'] / original_size[0] * original_size[1]

                main_window['SLIDER_Y'].update(int(y_res))
                current_res = (int(values['SLIDER_X']), int(y_res))
            else:
                current_res = (int(values['SLIDER_X']), int(values['SLIDER_Y']))

            img = original_image

            imgSmall = img.resize(current_res, resample=Image.Resampling.NEAREST)
            img = imgSmall.resize(real_size, Image.Resampling.NEAREST)

            if flag_recolored:
                img = img.convert('P', palette=Image.ADAPTIVE, colors=int(values['SLIDER_COLOR']))

            draw_figure(main_window['IMAGE'], img)
            debug(main_window, f'resized image to {current_res}')
            flag_resized = True

        if event == 'SLIDER_Y':
            if values['BUTTON_RATIO']:
                x_res = values['SLIDER_Y'] / original_size[1] * original_size[0]

                main_window['SLIDER_X'].update(int(x_res))
                current_res = (int(x_res), int(values['SLIDER_Y']))
            else:
                current_res = (int(values['SLIDER_X']), int(values['SLIDER_Y']))

            imgSmall = original_image.resize(current_res, resample=Image.Resampling.NEAREST)  #or BILINEAR?
            img = imgSmall.resize(real_size, Image.Resampling.NEAREST)

            if flag_recolored:
                img = img.convert('P', palette=Image.ADAPTIVE, colors=int(values['SLIDER_COLOR']))

            draw_figure(main_window['IMAGE'], img)
            debug(main_window, f'resized image to {current_res}')
            flag_resized = True

        if event == 'SLIDER_COLOR':
            img = original_image

            if flag_resized:
                current_res = (int(values['SLIDER_X']), int(values['SLIDER_Y']))  # będzie ok bo
                imgSmall = original_image.resize(current_res, resample=Image.Resampling.NEAREST)  # or BILINEAR?
                img = imgSmall.resize(real_size, Image.Resampling.NEAREST)
            else:
                if original_size[0] > 512 or original_size[1] > 512:
                    ratio = max(original_size[0], original_size[1]) / 512
                    real_size = (int(original_size[0] / ratio), int(original_size[1] / ratio))
                    img = original_image.resize(real_size, resample=Image.Resampling.NEAREST)

            img = img.convert('P', palette=Image.ADAPTIVE, colors=int(values['SLIDER_COLOR']))
            draw_figure(main_window['IMAGE'], img)
            debug(main_window, f'Reduced number of colors')
            flag_recolored = True

        if event == "RESET":
            if original_size[0] > img_size or original_size[1] > img_size:
                ratio = max(original_size[0], original_size[1]) / img_size
                real_size = (int(original_size[0] / ratio), int(original_size[1] / ratio))
                current_img = original_image.resize(real_size, resample=Image.Resampling.NEAREST)
            draw_figure(main_window['IMAGE'], current_img)
            debug(main_window, f'reset image to {real_size}')
            flag_resized = False
            flag_recolored = False
            main_window['SLIDER_X'].update(int(1024))
            main_window['SLIDER_Y'].update(int(1024))

        if event == "ROTATE_LEFT":
            original_image = original_image.rotate(90, expand=True)
            original_size = real_size = (original_size[1], original_size[0])
            temp = values['SLIDER_X']
            main_window['SLIDER_X'].update(int(values['SLIDER_Y']))
            main_window['SLIDER_Y'].update(int(temp))
            current_res = (int(values['SLIDER_Y']), int(values['SLIDER_X']))

            if original_size[0] > img_size or original_size[1] > img_size:
                ratio = max(original_size[0], original_size[1]) / img_size
                real_size = (int(original_size[0] / ratio), int(original_size[1] / ratio))
            imgSmall = original_image.resize(current_res, resample=Image.Resampling.NEAREST)
            img = imgSmall.resize(real_size, Image.Resampling.NEAREST)

            if flag_recolored:
                img = img.convert('P', palette=Image.ADAPTIVE, colors=int(values['SLIDER_COLOR']))
            #draw_figure(main_window['IMAGE'], original_image)
            draw_figure(main_window['IMAGE'], img)
            debug(main_window, f'resized image to {current_res}')

        if event == "ROTATE_RIGHT":
            original_image = original_image.rotate(-90, expand=True)
            original_size = real_size = (original_size[1], original_size[0])
            temp = values['SLIDER_X']
            main_window['SLIDER_X'].update(int(values['SLIDER_Y']))
            main_window['SLIDER_Y'].update(int(temp))
            current_res = (int(values['SLIDER_Y']), int(values['SLIDER_X']))

            if original_size[0] > img_size or original_size[1] > img_size:
                ratio = max(original_size[0], original_size[1]) / img_size
                real_size = (int(original_size[0] / ratio), int(original_size[1] / ratio))
            imgSmall = original_image.resize(current_res, resample=Image.Resampling.NEAREST)
            img = imgSmall.resize(real_size, Image.Resampling.NEAREST)

            if flag_recolored:
                img = img.convert('P', palette=Image.ADAPTIVE, colors=int(values['SLIDER_COLOR']))
            draw_figure(main_window['IMAGE'], img)
            debug(main_window, f'resized image to {current_res}')

        if event == 'ENTER_RES':
            if values['INPUT_X'] and values['INPUT_Y']:
                main_window['SLIDER_X'].update(int(values['INPUT_X']))
                main_window['SLIDER_Y'].update(int(values['INPUT_Y']))
            elif values['INPUT_X'] and values['BUTTON_RATIO'] and not values['INPUT_Y']:
                y_res = values['SLIDER_X'] / original_size[0] * original_size[1]
                main_window['SLIDER_Y'].update(int(y_res))
            elif values['INPUT_Y'] and values['BUTTON_RATIO'] and not values['INPUT_X']:
                x_res = values['SLIDER_Y'] / original_size[1] * original_size[0]
                main_window['SLIDER_X'].update(int(x_res))
            else:
                continue

            current_res = (int(values['SLIDER_X']), int(values['SLIDER_Y']))
            imgSmall = original_image.resize(current_res, resample=Image.Resampling.NEAREST)  # or BILINEAR?
            img = imgSmall.resize(real_size, Image.Resampling.NEAREST)

            if flag_recolored:
                img = img.convert('RGB', palette=Image.ADAPTIVE, colors=int(values['SLIDER_COLOR']))
            draw_figure(main_window['IMAGE'], img)
            debug(main_window, f'resized image to {current_res}')
            flag_resized = True


if __name__ == '__main__':
    #mode = '4k'   # otherwise 4k mode
    mode = 'riddles'
    main(mode)
