from argparse import ArgumentParser, Namespace
from match import MPDA, WPDA, MatchAlgorithms
from dynamics import Dynamics


parser = ArgumentParser(__doc__)
parser.add_argument("-a", "--algorithm", dest='algorithm',
                    default=MatchAlgorithms.MPDA,
                    choices=MatchAlgorithms.__members__.values(),
                    help="The algorithm to run.")
parser.add_argument("-s", "--size", type=int,
                    dest='size',
                    default=10, help="Population size")
parser.add_argument("--dynamics", default=Dynamics.STATIC,
                    choices=Dynamics.__members__.values(),
                    help='Dynamics type')


def main(args: Namespace):
    ...


if __name__ == "__main__":
    args = parser.parse_args()
    main(args)
