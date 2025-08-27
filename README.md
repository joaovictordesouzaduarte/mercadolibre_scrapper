# MercadoLibre Scraper

A powerful web scraping solution for extracting product data from MercadoLibre (Mercado Livre) using Selenium and AWS Lambda. This project provides automated data extraction capabilities for e-commerce analysis and monitoring.

## 🚀 Features

- **Automated Web Scraping**: Uses Selenium WebDriver with Chrome in headless mode
- **AWS Lambda Integration**: Deployable as a serverless function
- **Data Export**: Exports scraped data to CSV format
- **S3 Integration**: Automatically uploads results to AWS S3
- **Docker Support**: Containerized deployment with Chrome dependencies
- **Terraform Infrastructure**: Infrastructure as Code for AWS resources

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   MercadoLibre │    │   AWS Lambda    │    │   S3 Bucket     │
│   Website      │◄──►│   Function      │───►│   (Data Store)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   Chrome       │
                       │   Headless     │
                       └─────────────────┘
```

## 📋 Prerequisites

- Python 3.10+
- Docker
- AWS CLI configured
- Terraform (for infrastructure deployment)
- Chrome/Chromium browser

## 🛠️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/joaovictordesouzaduarte/mercadolibre_scrapper
cd mercadolibre_scrapper
```

### 2. Set Up Python Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r scripts/requirements.txt
```

### 3. AWS Configuration
- First, log in to the AWS Console and create a new ECR (Elastic Container Registry) repository named `mercadolibre-scrapper-repository`.

- Ensure that you have the AWS CLI installed on your local machine before proceeding.
#### How to Install AWS CLI

You need the AWS CLI to interact with AWS services. Follow the instructions below for your operating system:

<details>
<summary><strong>Windows</strong></summary>

1. **Download the AWS CLI MSI Installer:**

   [Download AWS CLI for Windows (64-bit)](https://awscli.amazonaws.com/AWSCLIV2.msi)

2. **Run the Installer:**

   Double-click the downloaded `.msi` file and follow the on-screen instructions.

3. **Verify Installation:**

   Open Command Prompt and run:
   ```cmd
   aws --version
   ```
   You should see the AWS CLI version output.
</details>

<details>
<summary><strong>macOS</strong></summary>

1. **Using Homebrew (recommended):**
   ```bash
   brew install awscli
   ```

2. **Or, use the bundled installer:**
   ```bash
   curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"
   sudo installer -pkg AWSCLIV2.pkg -target /
   ```

3. **Verify Installation:**
   ```bash
   aws --version
   ```
</details>

<details>
<summary><strong>Linux</strong></summary>

1. **Download the AWS CLI installer:**
   ```bash
   curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
   ```

2. **Unzip the installer:**
   ```bash
   unzip awscliv2.zip
   ```

3. **Run the install script:**
   ```bash
   sudo ./aws/install
   ```

4. **Verify Installation:**
   ```bash
   aws --version
   ```
</details>

- **How to get your AWS Secret Access Key:**  
  1. Sign in to the [AWS Management Console](https://console.aws.amazon.com/).  
  2. Click on your account name (top right) and select **Security Credentials**.  
  3. Under **Access keys**, click **Create access key**.  
  4. Download or copy your **Access key ID** and **Secret access key**.  
  > ⚠️ **Note:** You can only view your secret access key once when you create it. Store it securely.

- After that, you're able to interact with AWS services

- **How to configure AWS CLI on your local machine**

```bash
# Configure AWS credentials
aws configure
```
- Fill your credentails
- After that, execute the follow command

```bash
aws --version
```
- If you see something like the image bellow, you're ready

![Project Architecture](image.png)
## 🏁 How to Start the Project

Follow these steps to get the project up and running:

1. **Set Up Environment Variables**

   Create a `.env` file in the root directory with your AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION = us-east-2 end TERRAFORM_VERSION=1.6.6.

2. **Docker Usage**

   To run the project in a Docker container, follow the steps bellow:

    1. **Build the scrapper container:**
   ``` bash
   sudo docker build -t mercadolibre_scrapper:latest -f Dockerfile.lambda .
   ```
    2. **Tag the imagem and push to the AWS ECR:**
   
   ```bash     
        sudo docker tag YOUR-CONTAINER-ID YOUR-AWS-ACCOUNT-ID.dkr.ecr.us-east-2.amazonaws.com/mercadolibre-scrapper-repository
    ```

7. **(Optional) Deploy to AWS Lambda**

   Use Terraform or the AWS CLI to deploy the Lambda function as described in the sections below.

---

If you encounter any issues, please refer to the [Support](#-support) section or open an issue on GitHub.
<!-- ### 4. Environment Variables

Create a `.env` file in the root directory:

```env
AWS_REGION=us-east-1
S3_BUCKET_NAME=your-scraper-bucket
LAMBDA_FUNCTION_NAME=mercadolibre-scraper
```

## 🚀 Usage

### Local Development

```bash
# Run the scraper locally
python scripts/lambda_scrapper_mercadolibre.py
```

### Docker Deployment

```bash
# Build the Docker image
docker build -f Dockerfile.lambda -t mercadolibre-scraper .

# Run locally with Docker
docker run -e AWS_ACCESS_KEY_ID=your_key -e AWS_SECRET_ACCESS_KEY=your_secret mercadolibre-scraper
```

### AWS Lambda Deployment

```bash
# Deploy infrastructure with Terraform
cd terraform
terraform init
terraform plan
terraform apply

# Or deploy Lambda function directly
aws lambda create-function \
    --function-name mercadolibre-scraper \
    --runtime python3.10 \
    --role arn:aws:iam::your-account:role/lambda-execution-role \
    --handler lambda_scrapper_mercadolibre.lambda_handler \
    --zip-file fileb://deployment-package.zip
```

## 📊 Data Structure

The scraper extracts the following product information:

- Product name
- Price
- Seller information
- Product ratings
- Availability status
- Product URL
- Timestamp of extraction

## 🔧 Configuration

### Chrome Options

The scraper is configured with optimized Chrome options for AWS Lambda:

- Headless mode enabled
- GPU acceleration disabled
- Memory optimization settings
- Custom user agent
- Remote debugging port configuration

### Selenium Settings

- Implicit wait: 0 seconds (optimized for performance)
- Explicit wait: 12 seconds for critical elements
- Page source caching for analysis

## 📁 Project Structure

```
mercadolibre_scrapper/
├── scripts/
│   ├── lambda_scrapper_mercadolibre.py  # Main scraper logic
│   ├── install-browser.sh               # Browser installation script
│   ├── requirements.txt                 # Python dependencies
│   └── __init__.py
├── terraform/                           # Infrastructure as Code
├── Dockerfile.lambda                    # Lambda container definition
├── Dockerfile.terraform                 # Terraform container
├── chrome-deps.txt                      # Chrome dependencies
├── aws-configure-entrypoint.sh          # AWS configuration script
├── .gitignore                           # Git ignore rules
└── README.md                            # This file
```

## 🚨 Important Notes

- **Rate Limiting**: Be respectful of MercadoLibre's servers. Implement delays between requests if needed.
- **Legal Compliance**: Ensure your scraping activities comply with MercadoLibre's Terms of Service.
- **AWS Costs**: Monitor your Lambda function usage to avoid unexpected charges.
- **Data Privacy**: Handle scraped data according to applicable privacy regulations.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/your-username/mercadolibre_scrapper/issues) page
2. Create a new issue with detailed information
3. Contact the maintainers

## 🔄 Updates

Stay updated with the latest changes:

```bash
git pull origin main
pip install -r scripts/requirements.txt --upgrade
```

---

**Disclaimer**: This tool is for educational and research purposes. Users are responsible for ensuring compliance with applicable laws and website terms of service. -->