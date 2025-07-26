import streamlit as st

# Wheel layout & grouping
wheel_order = [
    32,15,19,4,21,2,25,17,34,6,27,
    13,36,11,30,8,23,10,5,24,16,33,1,
    20,14,31,9,22,18,29,7,28,12,35,3,26
]
group_map = {i+1: wheel_order[i*3:(i+1)*3] for i in range(12)}

def map_to_groups(numbers):
    groups = []
    for num in numbers:
        if num == 0: continue
        for g, vals in group_map.items():
            if num in vals: groups.append(g)
    return groups

def generate_seed(groups):
    return int("".join([str(g) for g in groups[-4:]]))

def kaprekar_steps(num):
    steps, seen = [], set()
    while num != 6174:
        digits = f"{num:04d}"
        asc = int("".join(sorted(digits)))
        desc = int("".join(sorted(digits, reverse=True)))
        num = desc - asc
        if num in seen or num == 0: return steps, False
        seen.add(num)
        steps.append((desc, asc, num))
    return steps, True

def predict_bets(seed):
    return [((int(d)%12)+1) for d in str(seed)[:3]]

# Streamlit app
def main():
    st.set_page_config(page_title="Kaprekar Roulette", layout="wide")

    # Sidebar
    bankroll = st.sidebar.number_input("Bankroll", min_value=0, value=120, step=1)
    st.sidebar.caption("Payout: 36 to 1 | Cost: 12/unit")

    # Session state
    for k in ["spins", "hits", "misses", "balance"]:
        if k not in st.session_state:
            st.session_state[k] = bankroll if k == "balance" else 0

    st.title("Kaprekar Roulette")
    nums = st.text_input("Enter 12 numbers", "32,15,19,4,21,2,25,17,34,6,27,13")
    parsed = [int(n.strip()) for n in nums.split(",") if n.strip().isdigit()]

    if st.button("Spin"):
        if len(parsed) != 12:
            st.error("Need exactly 12 numbers.")
            return

        groups = map_to_groups(parsed)
        if len(groups) < 4:
            st.warning("Not enough valid mappings.")
            return

        seed = generate_seed(groups)
        steps, valid = kaprekar_steps(seed)
        st.markdown(f"**Seed:** {seed}")

        for i, (d, a, r) in enumerate(steps, 1):
            st.write(f"{i}. {d} - {a} = {r}")

        st.session_state.spins += 1

        if valid:
            preds = predict_bets(steps[-1][2])
            st.markdown(f"**Predicted Groups:** {preds}")

            hit = any(p in groups[-3:] for p in preds)
            if hit:
                st.session_state.hits += 1
                st.session_state.balance += 24
                st.success("Hit! +24 units")
            else:
                st.session_state.misses += 1
                st.session_state.balance -= 12
                st.error("Missed. −12 units")
        else:
            st.warning("No Kaprekar convergence.")

    # Stats
    st.markdown("---")
    st.write(f"Balance: {st.session_state.balance} units")
    st.write(f"Spins: {st.session_state.spins} | Hits: {st.session_state.hits} | Misses: {st.session_state.misses}")

if __name__ == "__main__":
    main()
