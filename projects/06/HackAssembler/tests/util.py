def read_x_instructions(parser, x):
    for _ in range(x-1):
        parser.parse()
    return parser.parse()
