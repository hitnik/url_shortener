


from app.utils import parser


if __name__ == '__main__':
    parser = parser()
    args = parser.parse_args()
    print(args)
