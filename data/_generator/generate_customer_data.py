from __future__ import annotations

import argparse
import csv
import random
from collections import defaultdict
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path

FIRST_NAMES = [
    'Ava', 'Noah', 'Mia', 'Liam', 'Emma', 'Olivia', 'Ethan', 'Sophia', 'Lucas', 'Amelia',
    'Mason', 'Isabella', 'Logan', 'Harper', 'Elijah', 'Ella', 'James', 'Charlotte', 'Benjamin', 'Henry',
    'Evelyn', 'Alexander', 'Grace', 'Jack', 'Leo', 'Zoe', 'Nathan', 'Nora', 'Caleb', 'Ruby',
]

LAST_NAMES = [
    'Walker', 'Mitchell', 'Bennett', 'Carter', 'Parker', 'Turner', 'Collins', 'Ward', 'Reed', 'Baker',
    'Cooper', 'Murphy', 'Brooks', 'Morgan', 'Howard', 'Price', 'Ross', 'Kelly', 'Adams', 'Nelson',
    'Rivera', 'Campbell', 'Diaz', 'Sanchez', 'Foster', 'Gomez', 'Hughes', 'Long', 'Perry', 'Powell',
]

COMPANY_PREFIXES = ['North', 'Prime', 'Blue', 'Summit', 'Vertex', 'Pulse', 'Apex', 'Zenith', 'Nova', 'Harbor']
COMPANY_SUFFIXES = ['Retail', 'Systems', 'Group', 'Partners', 'Labs', 'Holdings', 'Network', 'Studio', 'Collective', 'Solutions']

REGIONS = [
    ('Northeast', ['Boston', 'New York', 'Philadelphia', 'Providence']),
    ('Southeast', ['Atlanta', 'Miami', 'Charlotte', 'Orlando']),
    ('Midwest', ['Chicago', 'Detroit', 'Columbus', 'Minneapolis']),
    ('Southwest', ['Dallas', 'Austin', 'Phoenix', 'Denver']),
    ('West', ['Seattle', 'Portland', 'San Francisco', 'Los Angeles']),
]

SEGMENTS = ['Enterprise', 'Mid-Market', 'SMB', 'Startup']
STATUS_WEIGHTS = [('Active', 0.72), ('At Risk', 0.18), ('Churned', 0.10)]
CHANNELS = ['Web', 'Mobile', 'Partner', 'Inbound', 'Event']
INDUSTRIES = ['Technology', 'Healthcare', 'Finance', 'Education', 'Retail', 'Manufacturing', 'Hospitality', 'Logistics']


@dataclass(frozen=True)
class Customer:
    customer_id: int
    first_name: str
    last_name: str
    company: str
    email: str
    phone: str
    region: str
    city: str
    state: str
    segment: str
    status: str
    channel: str
    industry: str
    signup_date: date
    last_order_date: date | None
    order_count: int
    lifetime_value: float
    average_order_value: float
    open_tickets: int
    satisfaction_score: float
    renewal_probability: float


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Generate random customer CSV data for dashboards and tables.')
    parser.add_argument('--rows', type=int, default=1500, help='Number of customer rows to generate (1000-2000 recommended).')
    parser.add_argument('--seed', type=int, default=42, help='Random seed for reproducible output.')
    parser.add_argument('--output-dir', default=str(Path(__file__).resolve().parents[1]), help='Directory to write CSV files to.')
    return parser.parse_args()


def choose_weighted_status(rng: random.Random) -> str:
    roll = rng.random()
    cumulative = 0.0
    for value, weight in STATUS_WEIGHTS:
        cumulative += weight
        if roll <= cumulative:
            return value
    return STATUS_WEIGHTS[-1][0]


def build_customer(customer_id: int, rng: random.Random) -> Customer:
    first_name = rng.choice(FIRST_NAMES)
    last_name = rng.choice(LAST_NAMES)
    company = f"{rng.choice(COMPANY_PREFIXES)} {rng.choice(COMPANY_SUFFIXES)}"
    region, cities = rng.choice(REGIONS)
    city = rng.choice(cities)
    state_map = {
        'Boston': 'MA', 'New York': 'NY', 'Philadelphia': 'PA', 'Providence': 'RI',
        'Atlanta': 'GA', 'Miami': 'FL', 'Charlotte': 'NC', 'Orlando': 'FL',
        'Chicago': 'IL', 'Detroit': 'MI', 'Columbus': 'OH', 'Minneapolis': 'MN',
        'Dallas': 'TX', 'Austin': 'TX', 'Phoenix': 'AZ', 'Denver': 'CO',
        'Seattle': 'WA', 'Portland': 'OR', 'San Francisco': 'CA', 'Los Angeles': 'CA',
    }
    state = state_map[city]
    segment = rng.choices(SEGMENTS, weights=[0.15, 0.28, 0.37, 0.20], k=1)[0]
    status = choose_weighted_status(rng)
    channel = rng.choice(CHANNELS)
    industry = rng.choice(INDUSTRIES)

    signup_date = date.today() - timedelta(days=rng.randint(30, 3650))
    order_count = max(0, int(rng.gauss(14, 9)))
    if status == 'Churned':
        order_count = max(1, int(order_count * 0.6))
    elif status == 'At Risk':
        order_count = max(1, int(order_count * 0.8))

    average_order_value = round(rng.uniform(45, 950) * {'Enterprise': 1.8, 'Mid-Market': 1.3, 'SMB': 1.0, 'Startup': 0.8}[segment], 2)
    lifetime_value = round(order_count * average_order_value * rng.uniform(0.9, 1.25), 2)
    open_tickets = rng.choices([0, 1, 2, 3, 4, 5], weights=[0.5, 0.18, 0.12, 0.09, 0.06, 0.05], k=1)[0]
    satisfaction_score = round(max(1.0, min(5.0, rng.gauss(4.1, 0.7) - (0.35 if status == 'At Risk' else 0.8 if status == 'Churned' else 0))), 1)
    renewal_probability = round(max(0.05, min(0.99, rng.gauss(0.78, 0.18) - (0.25 if status == 'Churned' else 0.1 if status == 'At Risk' else 0))), 2)

    last_order_date = None
    if order_count > 0:
        days_since_signup = max(7, (date.today() - signup_date).days)
        last_order_date = date.today() - timedelta(days=rng.randint(0, min(days_since_signup, 540)))

    email = f"{first_name.lower()}.{last_name.lower()}{customer_id % 97}@example.com"
    phone = f"({rng.randint(200, 999)}) {rng.randint(200, 999)}-{rng.randint(1000, 9999)}"

    return Customer(
        customer_id=customer_id,
        first_name=first_name,
        last_name=last_name,
        company=company,
        email=email,
        phone=phone,
        region=region,
        city=city,
        state=state,
        segment=segment,
        status=status,
        channel=channel,
        industry=industry,
        signup_date=signup_date,
        last_order_date=last_order_date,
        order_count=order_count,
        lifetime_value=lifetime_value,
        average_order_value=average_order_value,
        open_tickets=open_tickets,
        satisfaction_score=satisfaction_score,
        renewal_probability=renewal_probability,
    )


def write_customers_csv(path: Path, customers: list[Customer]) -> None:
    with path.open('w', newline='', encoding='utf-8') as handle:
        writer = csv.writer(handle)
        writer.writerow([
            'customer_id', 'first_name', 'last_name', 'company', 'email', 'phone', 'region', 'city', 'state',
            'segment', 'status', 'channel', 'industry', 'signup_date', 'last_order_date', 'order_count',
            'lifetime_value', 'average_order_value', 'open_tickets', 'satisfaction_score', 'renewal_probability',
        ])
        for customer in customers:
            writer.writerow([
                customer.customer_id,
                customer.first_name,
                customer.last_name,
                customer.company,
                customer.email,
                customer.phone,
                customer.region,
                customer.city,
                customer.state,
                customer.segment,
                customer.status,
                customer.channel,
                customer.industry,
                customer.signup_date.isoformat(),
                customer.last_order_date.isoformat() if customer.last_order_date else '',
                customer.order_count,
                f'{customer.lifetime_value:.2f}',
                f'{customer.average_order_value:.2f}',
                customer.open_tickets,
                f'{customer.satisfaction_score:.1f}',
                f'{customer.renewal_probability:.2f}',
            ])


def write_summary_csvs(output_dir: Path, customers: list[Customer]) -> None:
    by_region = defaultdict(lambda: {'customers': 0, 'revenue': 0.0, 'orders': 0, 'satisfaction_total': 0.0})
    by_segment = defaultdict(lambda: {'customers': 0, 'revenue': 0.0, 'orders': 0, 'renewal_total': 0.0})
    by_month = defaultdict(lambda: {'customers': 0, 'revenue': 0.0})

    for customer in customers:
        region_bucket = by_region[customer.region]
        region_bucket['customers'] += 1
        region_bucket['revenue'] += customer.lifetime_value
        region_bucket['orders'] += customer.order_count
        region_bucket['satisfaction_total'] += customer.satisfaction_score

        segment_bucket = by_segment[customer.segment]
        segment_bucket['customers'] += 1
        segment_bucket['revenue'] += customer.lifetime_value
        segment_bucket['orders'] += customer.order_count
        segment_bucket['renewal_total'] += customer.renewal_probability

        month_key = customer.signup_date.strftime('%Y-%m')
        month_bucket = by_month[month_key]
        month_bucket['customers'] += 1
        month_bucket['revenue'] += customer.lifetime_value

    with (output_dir / 'customer_summary_by_region.csv').open('w', newline='', encoding='utf-8') as handle:
        writer = csv.writer(handle)
        writer.writerow(['region', 'customers', 'total_revenue', 'total_orders', 'avg_satisfaction'])
        for region in sorted(by_region):
            bucket = by_region[region]
            writer.writerow([
                region,
                bucket['customers'],
                f"{bucket['revenue']:.2f}",
                bucket['orders'],
                f"{bucket['satisfaction_total'] / bucket['customers']:.2f}",
            ])

    with (output_dir / 'customer_summary_by_segment.csv').open('w', newline='', encoding='utf-8') as handle:
        writer = csv.writer(handle)
        writer.writerow(['segment', 'customers', 'total_revenue', 'total_orders', 'avg_renewal_probability'])
        for segment in sorted(by_segment):
            bucket = by_segment[segment]
            writer.writerow([
                segment,
                bucket['customers'],
                f"{bucket['revenue']:.2f}",
                bucket['orders'],
                f"{bucket['renewal_total'] / bucket['customers']:.2f}",
            ])

    with (output_dir / 'customer_summary_by_signup_month.csv').open('w', newline='', encoding='utf-8') as handle:
        writer = csv.writer(handle)
        writer.writerow(['signup_month', 'customers', 'total_revenue'])
        for month in sorted(by_month):
            bucket = by_month[month]
            writer.writerow([
                month,
                bucket['customers'],
                f"{bucket['revenue']:.2f}",
            ])


def main() -> None:
    args = parse_args()
    row_count = max(1000, min(2000, args.rows))
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    rng = random.Random(args.seed)
    customers = [build_customer(index + 1, rng) for index in range(row_count)]

    write_customers_csv(output_dir / 'customers.csv', customers)
    write_summary_csvs(output_dir, customers)

    print(f'Generated {row_count} customer rows in {output_dir / "customers.csv"}')
    print('Generated summary files: customer_summary_by_region.csv, customer_summary_by_segment.csv, customer_summary_by_signup_month.csv')


if __name__ == '__main__':
    main()