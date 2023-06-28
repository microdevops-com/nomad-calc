#!/usr/bin/python3

# Example of data structure is in example.yaml

import click
import yaml
import datetime
import pprint

@click.command()
@click.option("--yaml", "yaml_file", required=True, help="YAML file to parse")
# By default, the date is today
@click.option("--date", "on_date", default=None, help="Make calculations for this date in form of YYYY-MM-DD, default is today")
# Optional deug flag
@click.option("--debug", "debug", is_flag=True, default=False, help="Enable debug mode")
def main(yaml_file, on_date, debug):

    with open(yaml_file, "r") as stream:
        data = yaml.load(stream, Loader=yaml.SafeLoader)

    # If no on_date is given, use today for end date
    if on_date is None:
        on_date = datetime.date.today()
    else:
        on_date = datetime.datetime.strptime(on_date, "%Y-%m-%d").date()

    # Find the earliest entry_date in stays, it seems entry_date is already in datetime format after reading yaml
    start_date = min([stay["entry_date"] for stay in data["stays"]])

    # Find the latest exit_date in stays
    end_date = max([stay["exit_date"] for stay in data["stays"]])

    # https://stackoverflow.com/a/1060330
    def daterange(start_date, end_date):
        for n in range(int((end_date - start_date).days+1)):
            yield start_date + datetime.timedelta(n)

    # Empty dictionary to store the data per day
    day_data = {}

    # Walk through each day from start_date to end_date (inclusive) and initialize the dictionary for each day->nomad = empty list
    for day in daterange(start_date, end_date):
        day_data[day] = {}
        for nomad in data["nomads"]:
            day_data[day][nomad] = []

    # Walk through each stay and add the territories to the dictionary
    for stay in data["stays"]:
        for day in daterange(stay["entry_date"], stay["exit_date"]):
            for nomad in stay["nomads"]:
                # Add the territory to the list of territories for this nomad on this day if not already there
                if stay["territory"] not in day_data[day][nomad]:
                    day_data[day][nomad].append(stay["territory"])

    if debug:
        pprint.pprint(day_data)

    # Print on_date
    print("On Date: {on_date} (all dates are inclusive)".format(on_date=on_date))

    # For each nomad
    for nomad_name, nomad_params in data["nomads"].items():

        print("{nomad_name}:".format(nomad_name=nomad_name))

        # For each territory
        for territory_name, territory_params in data["territories"].items():

            days_sum = 0
            territory_check_start_date = on_date - datetime.timedelta(days=territory_params[nomad_params["nationality"]]["per_period"]-1)

            # Take period backwards from on_date to per_period for this nomad nationality on this territory
            for day in daterange(territory_check_start_date, on_date):

                # If nomad was on this territory on this day
                if day in day_data and territory_name in day_data[day][nomad_name]:

                    days_sum += 1

                    # Check if days_sum exceed maximum_stay
                    if days_sum > territory_params[nomad_params["nationality"]]["maximum_stay"]:
                        print("    {day}: already stayed {days} days from maximum stay of {maximum_stay} days".format(
                                day=day,
                                days=days_sum,
                                maximum_stay=territory_params[nomad_params["nationality"]]["maximum_stay"]
                            )
                        )


            print("  {territory_name} from {territory_check_start_date}: {days_sum}".format(
                    territory_name=territory_name,
                    territory_check_start_date=territory_check_start_date,
                    days_sum=days_sum
                )
            )

if __name__ == "__main__":
    main()
