using Iterators

# externally managed queue
external_queue = cycle(["A message", "Another, longer, second message", "hi"])

# display settings
screen_length = 30
gap_length = 6 # consider letting this be set externally, too

# on startup, message comes in from the right
padding = " "^(screen_length - gap_length)
internal_queue = chain([padding], external_queue)

# approximating the Python raster functions with text
image() = " "^screen_length
function draw!(img, text, offset)
    for i in max(1, 1 - offset) : min(length(text), length(img) - offset)
        img.data[i + offset] = text.data[i]
    end
end

# loop structure could simplified if we mandated a non-zero text/image width

live_messages = String[]
covered = 0
left_offset = 0

for msg in internal_queue

    push!(live_messages, msg)
    covered += length(msg) + gap_length
    left_length = length(live_messages[1])

    while covered >= screen_length
        img = image()

        offset = left_offset
        for msg in live_messages
           draw!(img, msg, offset)
           offset += length(msg) + gap_length
        end

        println(img)

        left_offset -= 1
        covered -= 1

        if -left_offset > left_length
            left_offset += left_length + gap_length
            shift!(live_messages)
            left_length = length(live_messages[1])
        end
    end
end
