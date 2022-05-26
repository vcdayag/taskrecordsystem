import database as db

from rich.console import Console
from rich.prompt import Prompt
from rich.columns import Columns
from rich.panel import Panel
from rich.text import Text
from rich.padding import Padding

console = Console()
lorem = "Lorem ipsum dolor sit amet consectetur adipisicing elit. Maxime mollitia, molestiae quas vel sint commodi repudiandae consequuntur voluptatum laborum numquam blanditiis harum quisquam eius sed odit fugiat iusto fuga praesentium optio, eaque rerum! Provident similique accusantium nemo autem. Veritatis obcaecati tenetur iure eius earum ut molestias architecto voluptate aliquam nihil, eveniet aliquid culpa officia aut! Impedit sit sunt quaerat, odit, tenetur error, harum nesciunt ipsum debitis quas aliquid."


def main():
    [console.print(Panel(Text(lorem, justify="left"),padding=(1,5),
                   title=x, title_align="left")) for x in db.test_data()]
    # name = Prompt.ask("Enter your name", choices=[
    #                   "Paul", "Jessica", "Duncan"], default="Paul")
    # print('Hello '+name)


if __name__ == '__main__':
    main()
