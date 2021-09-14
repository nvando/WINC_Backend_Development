# Do not modify these lines
__winc_id__ = "62311a1767294e058dc13c953e8690a4"
__human_name__ = "casting"

# Add your code after this line

leek = 2
leek_order = "leek 4"
leek_order_no = leek_order[leek_order.find(" ") + 1 :]
leek_order_no = int(leek_order_no)
sum_total = leek_order_no * leek

print("Leek is " + str(leek) + " euro per kilo.")
print(sum_total)

broccoli = 2.34
broccoli_order = "broccoli 1.6"
broccoli_order_no = broccoli_order[broccoli_order.find(" ") + 1 :]
broccoli_order_no = float(broccoli_order_no)
total_price = broccoli_order_no * broccoli

print(str(broccoli_order_no) + "kg broccoli costs " + str(round(total_price, 2)) + "e")
