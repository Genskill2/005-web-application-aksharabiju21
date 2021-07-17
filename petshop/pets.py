@bp.route("/search/<field>/<value>")
def search(field, value):
    # TBD
    return ""
    conn = db.get_db()
    cursor = conn.cursor()
    oby1 = request.args.get("order_by", "id")
    order = request.args.get("order", "asc")
    cursor.execute(f"select p.id, p.name, p.bought, p.sold, s.name from pet p, animal s where p.id IN (select tp.pet from tags_pets tp, tag t where t.name='%s' and tp.tag=t.id) and p.species = s.id order by p.id" % value)
    pets = cursor.fetchall()
    return render_template('search.html',pets=pets,order="desc" if order=="asc" else "asc")

@bp.route("/")
def dashboard():
    conn = db.get_db()
    cursor = conn.cursor()
    oby = request.args.get("order_by", "id") # TODO. This is currently not used. 

    #to sort by id
    oby1 = request.args.get("order_by", "id")  
    order = request.args.get("order", "asc")
    if order == "asc":
    if order == "asc" and oby1=="id":
        cursor.execute(f"select p.id, p.name, p.bought, p.sold, s.name from pet p, animal s where p.species = s.id order by p.id")
    else:
        pets = cursor.fetchall()
    elif oby1=="id":
        cursor.execute(f"select p.id, p.name, p.bought, p.sold, s.name from pet p, animal s where p.species = s.id order by p.id desc")
    pets = cursor.fetchall()
        pets = cursor.fetchall()

    #to sort by name
    oby2 = request.args.get("order_by", "name")
    if order == "asc" and oby2=="name":
        cursor.execute(f"select p.id, p.name, p.bought, p.sold, s.name from pet p, animal s where p.species = s.id order by p.name")
        pets = cursor.fetchall()
    elif oby2=="name":
        cursor.execute(f"select p.id, p.name, p.bought, p.sold, s.name from pet p, animal s where p.species = s.id order by p.name desc")
        pets = cursor.fetchall()

    #to sort by date of bought
    oby3 = request.args.get("order_by", "bought")
    if order == "asc" and oby3=="bought":
        cursor.execute(f"select p.id, p.name, p.bought, p.sold, s.name from pet p, animal s where p.species = s.id order by p.bought")
        pets = cursor.fetchall()
    elif oby3=="bought":
        cursor.execute(f"select p.id, p.name, p.bought, p.sold, s.name from pet p, animal s where p.species = s.id order by p.bought desc")
        pets = cursor.fetchall()

    #to sort by date of sold
    oby4 = request.args.get("order_by", "sold")
    if order == "asc" and oby4=="sold":
        cursor.execute(f"select p.id, p.name, p.bought, p.sold, s.name from pet p, animal s where p.species = s.id order by p.sold")
        pets = cursor.fetchall()
    elif oby4=="sold":
        cursor.execute(f"select p.id, p.name, p.bought, p.sold, s.name from pet p, animal s where p.species = s.id order by p.sold desc")
        pets = cursor.fetchall()

    #to sort by name of species
    oby5 = request.args.get("order_by", "species")
    if order == "asc" and oby5=="species":
        cursor.execute(f"select p.id, p.name, p.bought, p.sold, s.name from pet p, animal s where p.species = s.id order by s.name")
        pets = cursor.fetchall()
    elif oby5=="species":
        cursor.execute(f"select p.id, p.name, p.bought, p.sold, s.name from pet p, animal s where p.species = s.id order by s.name desc")
        pets = cursor.fetchall()

    return render_template('index.html', pets = pets, order="desc" if order=="asc" else "asc")


@@ -63,6 +108,7 @@ def edit(pid):
        cursor.execute("select t.name from tags_pets tp, tag t where tp.pet = ? and tp.tag = t.id", [pid])
        tags = (x[0] for x in cursor.fetchall())
        name, bought, sold, description, species = pet
        print(sold)
        data = dict(id = pid,
                    name = name,
                    bought = format_date(bought),
@@ -74,10 +120,25 @@ def edit(pid):
    elif request.method == "POST":
        description = request.form.get('description')
        sold = request.form.get("sold")
        # TODO Handle sold
        return redirect(url_for("pets.pet_info", pid=pid), 302)



        cursor.execute("select p.sold from pet p where p.id = ?", [pid])
        pet_sold = cursor.fetchone()
        sold_date, = pet_sold
        sql_update_query = """update pet set description = ?, sold = ? where id = ?"""

        if sold_date!='' and not sold:
            data = (description, '', pid)
            cursor.execute(sql_update_query, data)    
            conn.commit()

        if sold_date=='' and sold:
            today = datetime.date.today().strftime('%Y-%m-%d')
            data = (description, today, pid)
            cursor.execute(sql_update_query, data)    
            conn.commit()

        else:
            sql_update_query = """update pet set description = ? where id = ?"""
            data = (description, pid)
            cursor.execute(sql_update_query, data)    
            conn.commit()
        return redirect(url_for("pets.pet_info", pid=pid), 302)
        
    



