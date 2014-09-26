require 'rails_helper'

RSpec.describe HomeController, :type => :controller do

  describe "GET client" do
    it "returns http success" do
      get :client
      expect(response).to be_success
    end
  end

  describe "GET compute" do
    it "returns http success" do
      get :compute
      expect(response).to be_success
    end
  end

end
