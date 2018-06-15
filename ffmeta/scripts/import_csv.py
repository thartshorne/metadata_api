import os.path
import re
from csv import DictReader
from collections import Counter

from flask import current_app

import ffmeta
from ffmeta import create_app
from ffmeta.models import Variable, Topic, Group, Umbrella, Response
from ffmeta.models.db import session


def load_csv():
    '''Load metadata to the specified database.'''
    with open(os.path.join(os.path.dirname(ffmeta.__file__), current_app.config["METADATA_FILE"])) as t:
        rows = list(DictReader(t))
        vars_loaded = 0
        commit_increment = 1000
        group_ids = []
        umbrella_topics = set()
        for row in rows:
            # Determine group membership
            group_no = None
            group_sub = None
            groupclass = re.search("[A-z]+", str(row["group"]))
            if not groupclass:
                group_no = str(row["group"])
            else:
                group_sub = re.search("[A-z]+", str(row["group"])).group(0)
                group_no = str(row["group"]).replace(group_sub, "")

            # Write variable data
            var = Variable(name=row["new_name"],
                           label=row["varlab"].replace('"', "'"),
                           old_name=row["old_name"],
                           data_type=row["type"],
                           warning=int(row["warning"]),
                           group_id=group_no,
                           group_subid=group_sub,
                           data_source=row["source"],
                           respondent=row["respondent"],
                           wave=str(row["wave"]),
                           scope=str(row["scope"]),
                           section=row.get("section"),
                           leaf=str(row["leaf"]))
            session.add(var)

            # Write topic data
            # Also, save umbrella data (we add this table later)
            topic1 = Topic(name=row["new_name"], topic=row["topic1"])
            session.add(topic1)
            umbrella_topics.add((row["topic1"], row["umbrella1"]))
            if len(row["topic2"]) > 0:
                # Some rows have multiple topics (up to 2)
                topic2 = Topic(name=row["new_name"], topic=row["topic2"])
                session.add(topic2)
                umbrella_topics.add((row["topic2"], row["umbrella2"]))

            # Write response data
            for key in row.keys():
                if key.find("label") > -1 and len(row[key]) > 0:
                    # Clean up response label
                    respidx = key.replace("label", "")
                    try:
                        lab_pts = row[key].split(" ", 1)
                        lab_pref = lab_pts[0]
                        val = row["value" + respidx]
                        if lab_pref == val:
                            lab = lab_pts[1]  # Drop the prefix if it's the response value
                        else:
                            lab = row[key]
                    except IndexError:
                        lab = row[key]  # Default to the full entry if we can't clean up

                    # Append new response row
                    resp = Response(name=row["new_name"], label=lab, value=row["value" + respidx])
                    session.add(resp)

            # Add to group list
            group_ids.append(str(row["group"]))

            # Increment variable counter
            vars_loaded += 1

            # Commit in increments of k
            if vars_loaded % commit_increment == 0:
                session.commit()

        # Commit any remaining rows
        session.commit()

        # Build groups table
        # TODO: The groups quality is bad -- revisit this tomorrow
        groups = Counter(group_ids)
        for group_id, group_n in groups.items():
            grp = Group(group_id=group_id, count=group_n)
            session.add(grp)
        session.commit()

        # Build umbrellas table
        for topic, umbrella in umbrella_topics:
            umb = Umbrella(topic=topic, umbrella=umbrella)
            session.add(umb)
        session.commit()

    # Yield result
    return "Loaded {} rows to database.".format(str(vars_loaded))


if __name__ == '__main__':

    application = create_app(debug=True)
    with application.app_context():
        load_csv()
